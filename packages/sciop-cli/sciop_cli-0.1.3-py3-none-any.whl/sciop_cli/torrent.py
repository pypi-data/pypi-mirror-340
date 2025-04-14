import warnings
from math import floor
from pathlib import Path
from typing import Literal as L

import bencode_rs
import libtorrent
from pydantic import TypeAdapter
from tqdm import tqdm

from sciop_cli.const import DEFAULT_TORRENT_CREATOR, EXCLUDE_FILES
from sciop_cli.exceptions import NoTrackersWarning
from sciop_cli.types import PieceSize


def estimate_piece_size(
    data_size: int, min_pieces: int = 2000, min_piece_size: int = 256 * (2**10)
) -> int:
    """
    Estimate the best piece size given some total size (in bytes) of a torrent

    Largest piece size that still gives us min_pieces.
    Files smaller than the piece size will be packed together into archives,
    so padding files are not much of an overhead concern here.

    pieces = ceil(size / (multiplier * 16KiB))
    pieces * (multiplier * 16KiB) = size
    multiplier = floor(size / (pieces * 16KiB))

    """
    block = 16 * (2**10)
    multiplier = floor(data_size / (min_pieces * block))
    piece_size = round(multiplier * block)
    return max(piece_size, min_piece_size)


def create_torrent(
    path: Path,
    trackers: list[str] | None = None,
    comment: str | None = None,
    creator: str = DEFAULT_TORRENT_CREATOR,
    webseeds: list[str] | None = None,
    similar: list[str] | None = None,
    version: L["v1", "v2", "hybrid"] = "hybrid",
    bencode: bool = True,
    piece_size: PieceSize = 512 * (2**10),
    pbar: bool = False,
) -> dict | bytes:
    """
    Create a hybrid v1/v2 torrent with libtorrent

    Args:
        path: File or directory to create a torrent for
        trackers: list of trackers to add to the torrent.
            Each torrent is added on a separate tier, in order,
            so that by default clients announce to all trackers
        comment: Additional comment string embedded in the torrent
        creator: Annotation of what tool was used to create the torrent,
            defaults to `sciop-cli-{version}`
        webseeds: List of HTTP urls where the content can also be found.
            If `path` is a directory, the files on the server
            must match the directory structure of the torrent and their content exactly.
        similar: Infohashes of torrents that have identical files to those in this torrent.
            Clients can use this to deduplicate downloads.
        version: Torrent version to create. Default ``"hybrid"`` creates v1/v2 compatible torrents.
            v1 is *not recommended.*
        bencode: If ``True`` ( default ) return the bencoded bytestring.
            Otherwise return a python dictionary
        piece_size: The size of data chunks to hash.
            Choosing a piece size can be complicated, but ideally you want
            to pick a piece size that yields 20-50k pieces, and less than <100k.
            Smaller torrents can have fewer pieces, in that case match the piece size
            to being slightly smaller than the median file size.
            Once torrents start to have >200k pieces, clients suffer to efficiently
            track which peers have what pieces, and also struggle to cache the data.
        pbar: It ``True``, show a progress bar while hashing pieces.

    Returns:
        bytes: bencoded torrent ready for writing
        dict: python-formatted torrent file dict
    """
    path = Path(path)
    fs = libtorrent.file_storage()

    if path.is_dir():
        # get paths and sort
        paths = []
        for _path in path.rglob("*"):
            if _path.name not in EXCLUDE_FILES and _path.is_file():
                # no absolute paths in the torrent plz
                rel_path = _path.relative_to(path)
                # add the parent again as the root
                rel_path = Path(path.name) / rel_path
                paths.append((str(rel_path), _path.stat().st_size))
        paths = sorted(paths, key=lambda x: x[0])
        for p, size in paths:
            fs.add_file(p, size)

    else:
        fs.add_file(path.name, path.stat().st_size)

    if fs.num_files() == 0:
        raise

    piece_size = TypeAdapter(PieceSize).validate_python(piece_size)

    flags = 0
    if version == "v1":
        flags = libtorrent.create_torrent.v1_only
    elif version == "v2":
        flags = libtorrent.create_torrent.v2_only

    torrent = libtorrent.create_torrent(fs, piece_size=piece_size, flags=flags)

    if trackers:
        for tier, tracker in enumerate(trackers):
            torrent.add_tracker(tracker, tier)
    else:
        warnings.warn(
            "No trackers passed when creating a torrent. "
            "This torrent will likely not be able to be seeded efficiently. "
            "Consider adding trackers, or use the default trackers "
            "(with `sciop_cli.data.get_default_trackers()`)",
            NoTrackersWarning,
            stacklevel=2,
        )

    if webseeds:
        for webseed in webseeds:
            torrent.add_url_seed(webseed)

    if similar:
        for s in similar:
            torrent.add_similar_torrent(s)

    if comment:
        torrent.set_comment(comment)

    torrent.set_creator(creator)

    _pbar = None
    if pbar:
        _pbar = tqdm(desc="hashing pieces...", total=torrent.num_pieces())

        def _pbar_callback(piece_index: int) -> None:
            _pbar.update()

        libtorrent.set_piece_hashes(torrent, str(path.parent.resolve()), _pbar_callback)
        _pbar.close()
    else:
        libtorrent.set_piece_hashes(torrent, str(path.parent.resolve()))

    ret = torrent.generate()
    if bencode:
        return bencode_rs.bencode(ret)
    else:
        return ret
