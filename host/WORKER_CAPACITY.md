# Read worker memory and filesystem capacity

`host/worker_capacity.py` prints one read-only JSON snapshot for choosing the next local job. It uses Python's standard library and creates no files. Pass each existing output directory or file whose filesystem matters; the default is the current directory.

```sh
python3 -B host/worker_capacity.py --path . --path /dev/shm
```

For an output that does not exist yet, pass its existing parent. Several paths on the same filesystem remain separate observations. The command does not walk directory contents, inspect other workers' processes, reserve capacity, change resource limits, delete files or start a monitor.

## Read the fields

| Field | Meaning |
| --- | --- |
| `host_memory.available_bytes` | Linux `/proc/meminfo` host availability; this does not incorporate the process's cgroup limit. |
| `cgroup_memory.levels` | Current cgroup and each ancestor visible through its cgroup v2 mount, with charged memory, hard limit and high setting. |
| `levels[].headroom_bytes` | Nonnegative difference between a readable finite `memory.max` and that level's `memory.current`. |
| `smallest_observed_headroom_bytes` | Smallest of those observed differences; `null` when no readable finite limit supplies one. |
| `max_status` / `high_status` | `finite`, `unlimited` for the kernel's `max` value, or `unavailable`. Unknown readings remain `null`. |
| `cgroup_memory.events` | Current cumulative memory-event counters. One reading is neither a rate nor an attribution to a particular worker. |
| `cgroup_memory.stat_bytes` | Selected anonymous, file, shared-memory, kernel and inactive-file counters. These overlap; do not sum them. |
| `filesystems[].available_bytes` | Filesystem space available to the caller, excluding reserved blocks where `statvfs` is available. |
| `inodes_available` / `inodes_total` | Native inode counts when supported; separate from byte capacity. |
| `started_at` / `finished_at` | UTC bounds around the sequential reads. |

Read host availability, cgroup headroom and filesystem space together. A memory-backed filesystem consumes memory as well as its own space. Reclaim, other workers, hidden ancestors, swap policy and concurrent allocation can affect what a new job can actually use. The snapshot is observational and does not promise an allocation will succeed. The cgroup metric deliberately names only the visible, readable hierarchy.

## Platform and error behavior

Memory reporting uses Linux procfs and cgroup v2. Membership is resolved against the process's visible mount table, including mount-root offsets and escaped mount paths. Ancestors are read only up to that mount. A missing controller, hidden/unresolvable mount or unreadable field is explicit `unavailable` or `partial`; it never becomes a zero-byte reading or an unlimited limit. Other platforms can still return filesystem bytes while their Linux memory readings are unavailable. Native execution has been performed on the current Linux cloud VM; other operating systems and cgroup v1 are not claimed validated.

Exit `0` means the requested filesystem observations completed and the report was printed. It does not mean memory is sufficient or that every optional memory field was readable. An invalid argument or inaccessible requested filesystem returns `2`; filesystem errors remain in the JSON alongside any successful observations. Redirect stdout only to a destination you intend to write and that has room for the report.

The schema is `commons.worker_capacity/v1`. The command has no dependencies, background jobs, provider calls or integration with task dispatch.

## Sources

- [Linux cgroup v2 documentation](https://docs.kernel.org/admin-guide/cgroup-v2.html#memory-interface-files): memory counters, limits and hierarchical accounting.
- [Linux mountinfo format](https://man7.org/linux/man-pages/man5/proc_pid_mountinfo.5.html): mount roots, mount points and filesystem types.
