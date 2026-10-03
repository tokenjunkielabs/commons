# Read worker memory and filesystem capacity

`host/worker_capacity.py` prints one read-only JSON snapshot for choosing the next local job. It uses Python's standard library and creates no files. Pass each existing output directory or file whose filesystem matters; the default is the current directory.

```sh
python3 -B host/worker_capacity.py --path . --path /dev/shm
```

For an output that does not exist yet, pass its existing parent. Several paths on the same filesystem remain separate observations. The default command does not walk directory contents or read individual process status files. The optional process view below reads bounded procfs status files. Neither mode reserves capacity, changes resource limits, deletes files or starts a monitor.

## Read the fields

| Field | Meaning |
| --- | --- |
| `host_memory.available_bytes` | Linux `/proc/meminfo` host availability; this does not incorporate the process's cgroup limit. |
| `cgroup_memory.levels` | Current cgroup and each ancestor visible through its cgroup v2 mount, with charged memory, hard limit and high setting. |
| `levels[].headroom_bytes` | Nonnegative difference between a readable finite `memory.max` and that level's `memory.current`. |
| `smallest_observed_headroom_bytes` | Smallest of those observed differences; `null` when no readable finite limit supplies one. |
| `max_status` / `high_status` | `finite`, `unlimited` for the kernel's `max` value, or `unavailable`. Unknown readings remain `null`. |
| `cgroup_memory.events` | Current cumulative memory-event counters. One reading is neither a rate nor an attribution to a particular worker. |
| `cgroup_memory.stat_bytes` | Selected anonymous, file, shared-memory and kernel counters, file activity and slab breakdown. These overlap; do not sum them. |
| `cgroup_memory.pressure` | Current cgroup's native `memory.pressure` reading, its source path and status; unavailable values remain `null`. |
| `pressure.some` / `pressure.full` | Time with at least some tasks stalled on memory, or all non-idle tasks stalled simultaneously. |
| `avg10_percent` / `avg60_percent` / `avg300_percent` | Kernel pressure trends over ten, sixty and three hundred seconds, in percent. |
| `total_us` | Cumulative stall time in microseconds, not bytes or a count of failures. |
| `filesystems[].available_bytes` | Filesystem space available to the caller, excluding reserved blocks where `statvfs` is available. |
| `inodes_available` / `inodes_total` | Native inode counts when supported; separate from byte capacity. |
| `started_at` / `finished_at` | UTC bounds around the sequential reads. |

Read host availability, cgroup headroom and filesystem space together. A memory-backed filesystem consumes memory as well as its own space. Reclaim, other workers, hidden ancestors, swap policy and concurrent allocation can affect what a new job can actually use. The snapshot is observational and does not promise an allocation will succeed. The cgroup metric deliberately names only the visible, readable hierarchy.

### Interpret reclaim and stalls together

The slab fields distinguish total in-kernel object storage (`slab`), the portion the kernel may reclaim (`slab_reclaimable`) and the portion it cannot reclaim under memory pressure (`slab_unreclaimable`). A reclaimable counter is not a promise that the bytes can be allocated now. Do not add it to headroom or subtract it from charged memory as a guaranteed availability estimate.

The file fields include `active_file`, `inactive_file`, `file_mapped`, `file_dirty` and `file_writeback`. Active and inactive counts describe reclaim-list state; they need not sum to the type-based `file` counter. Dirty bytes have not yet been written back; writeback bytes are currently being written. These are separate native observations, not an automatic cleanup recommendation.

Pressure complements charged bytes by describing stalls already experienced in the current cgroup. It does not attribute stalls to a worker, forecast the next allocation or report hidden ancestors. `full` is a subset of `some`; do not sum them. No pressure read registers a trigger or starts a monitor.

## Optional visible process RSS

Use the opt-in process view when the charged memory needs context from the processes visible to this command:

```sh
python3 -B host/worker_capacity.py --path . --path /dev/shm --process-rss
```

Only this option adds the `process_rss` object. The default fields and filesystem-based exit behavior stay the same. The scan reads `/proc` directory entries and each selected numeric PID's `status` file. Each returned process has exactly `pid`, `parent_pid`, `name` (the kernel's short process name) and `rss_bytes`. It does not read command lines, environment variables, open files or detailed memory maps, infer worker ownership, or control processes. Rows are ordered by observed RSS descending, with unknown values last; a bounded subset is not a claim about the largest processes outside that subset.

`--max-processes` bounds status-file attempts (default 256, range 1–4096). `--max-process-bytes` bounds all bytes actually returned by status-file reads (default 1,048,576, range 1–8,388,608). Each individual file is additionally bounded to 65,536 bytes, and directory enumeration is bounded to `max_processes + 1024` entries, including non-PID entries. Those arguments only affect the optional scan. The command stops conservatively when a bound is reached before EOF is observed; it does not assume an exact-boundary file or directory was complete.

| Process field | Meaning |
| --- | --- |
| `status` | `ok` for a completed enumeration with readable RSS for every observed PID; `partial` for a bound, vanished/unreadable/malformed status or missing RSS; `unavailable` if directory access fails before any status attempt. |
| `rss_sum_bytes` | Sum of the returned, readable RSS values; `null` if there are none. Unknown processes do not become zero-byte readings. |
| `coverage` limits and counts | Declared process, directory and byte limits; observed entries, attempted files, consumed bytes, returned rows and rows with RSS. |
| `enumeration_complete` | Whether the directory iterator reached EOF during this sequential observation; it does not certify an atomic snapshot. |
| `stop_reason` / `pending_pid` | A limiting condition and, when discovered but not attempted, the next PID. An interrupted file is identified separately. |
| `unavailable_status_files` | PID and error kind/errno for a status file that vanished, could not be read or could not be interpreted. |
| `truncated_status_files` | PID, reason and consumed bytes for each status file that did not reach EOF within the remaining bounds. |
| `missing_rss_pids` | Returned processes whose status omits `VmRSS`; their `rss_bytes` stays `null`. |

The process scope is the visible procfs namespace, which may differ from the current cgroup. Processes can exit or reuse PIDs between reads, and the observer itself can appear. Kernel RSS accounting is approximate and sums can count shared resident pages in several processes. The sum therefore neither explains all cgroup charge nor predicts bytes available after a process exits. Read it alongside the existing file/shared-memory/slab counters; do not subtract it from cgroup usage as an exact attribution or add it to headroom.

## Recover capacity from closed tmpfs data

Large retained captures, decoded media and dependency trees can occupy a memory-backed filesystem after their processes finish. When disk-backed scratch has enough bytes and inodes, use it for new large intermediates. Existing closed data can be relocated while keeping its contents and original paths usable.

1. Read the existing capacity command before choosing a source and destination. Confirm the destination's actual mount, available bytes and inodes; changing a pathname alone does not move data off tmpfs. Budget for the destination copy and temporary page-cache growth.
2. Select only data you own whose executions and consumers are independently recorded as closed. The optional RSS list does not establish directory ownership or prove that files are unused. Record unavailable process reads as unavailable; leave shared or uncertain trees in place.
3. Copy one selected tree at a time. Record regular-file hashes and sizes, file types, modes, ownership, timestamps and symlink targets. Account for hard links and unsupported entries before selecting the tree. Keep source, evidence, databases and reusable dependencies in the retained copy.
4. Compare the copied manifest and recheck source stability before releasing the original tmpfs allocation. Preserve original paths with compatible symlinks where required, and check any linked Git worktree still resolves to the same HEAD and worktree state. Retain the source when copying, comparison or compatibility fails.
5. Close the copy and verification work, then read capacity again. Report logical file sizes separately from measured allocated blocks. A fall in tmpfs usage need not immediately increase cgroup headroom: copying and hashing can populate disk-backed page cache.

### Optional file-specific cache hints

For verified disk copies that will remain closed, Linux can be given a `POSIX_FADV_DONTNEED` hint for each selected regular file. Use the resolved disk target from the verified list, rather than its compatibility symlink. Open it with `os.O_RDONLY | os.O_NOFOLLOW`, check its identity and metadata against the completed copy, call `os.fsync(fd)` followed by `os.posix_fadvise(fd, 0, 0, os.POSIX_FADV_DONTNEED)`, recheck identity and metadata, and close the descriptor even if an operation fails. Preserve per-file errors and skip a file whose identity changed.

The hint asks the kernel to release cached pages for that file; it does not remove file contents. Zero length addresses the remainder of the file, and the preceding sync makes dirty data eligible for consideration. The hint is nonbinding, partial pages may remain cached, and availability depends on the platform. Scope it to the independently closed, verified files; the capacity command itself stays read-only and performs no relocation or cache action. Avoid an immediate checksum reread when measuring the hint's effect, because reading contents can repopulate the cache.

In the completed 2026-10-03 cloud operation, 10,129 regular files containing 517,848,521 logical bytes were retained across serialized relocations. The subsequent file-specific hint pass observed cgroup charge fall from 8,371,130,368 to 7,817,707,520 bytes while shared-memory charge remained 4,665,241,600 bytes and the cumulative OOM-kill count remained 24. These are dated, concurrent observations, not a per-file allocation guarantee. The [relocation record](https://tokenjunkielabs.slack.com/archives/C0BU51F1PL3/p1791059251188019) and [cache-hint follow-through](https://tokenjunkielabs.slack.com/archives/C0BU51F1PL3/p1791059640225439) describe the retained data and measurement limits.

## Platform and error behavior

Memory reporting uses Linux procfs and cgroup v2. Membership is resolved against the process's visible mount table, including mount-root offsets and escaped mount paths. Ancestors are read only up to that mount. A missing controller, hidden/unresolvable mount or unreadable field is explicit `unavailable` or `partial`; it never becomes a zero-byte reading or an unlimited limit. The pressure file is optional: missing, unreadable or malformed input has its own source, unavailable status and error, and makes the cgroup summary partial while preserving the readable limits and counters. Other platforms can still return filesystem bytes while their Linux memory readings are unavailable. Native execution has been performed on the current Linux cloud VM, including its live slab/file counters and the absent-pressure-file path. This VM does not expose `memory.pressure`; successful PSI parsing on a PSI-enabled kernel is not claimed as a native result. Other operating systems and cgroup v1 are not claimed validated.

Exit `0` means the requested filesystem observations completed and the report was printed. It does not mean memory is sufficient or that every optional memory field was readable. An invalid argument or inaccessible requested filesystem returns `2`; filesystem errors remain in the JSON alongside any successful observations. Redirect stdout only to a destination you intend to write and that has room for the report.

The schema is `commons.worker_capacity/v1`. The command has no dependencies, background jobs, provider calls or integration with task dispatch.

## Sources

- [Linux cgroup v2 documentation](https://docs.kernel.org/admin-guide/cgroup-v2.html#memory-interface-files): memory counters, limits and hierarchical accounting.
- [Linux pressure-stall documentation](https://docs.kernel.org/accounting/psi.html): cgroup pressure format, stall classes, percentage windows and microsecond totals.
- [Linux mountinfo format](https://man7.org/linux/man-pages/man5/proc_pid_mountinfo.5.html): mount roots, mount points and filesystem types.
- [Linux procfs documentation](https://docs.kernel.org/filesystems/proc.html): visible process status, PID lifetime, short names, RSS fields and shared-memory accounting.
- [Python file advice API](https://docs.python.org/3/library/os.html#os.posix_fadvise): file-descriptor advice and platform availability.
- [Linux posix_fadvise manual](https://man7.org/linux/man-pages/man2/posix_fadvise.2.html): nonbinding hints, whole-file ranges, partial pages and dirty-page handling.
