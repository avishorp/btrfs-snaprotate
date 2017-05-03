btrfs_snaprotate
================

## Description
btrfs_snaprotate is a tool for creating and rotating BTRFS snapshots. It can designed to be used to create
time-based snapshots of BTRFS subvolumes and delete old ones, so only a specified number of snapshots
remain. It is designed to be used in conjunction with a time based scheduling system (such as cron),
but can also be used with event-based scheduling or manually.

## Installation
TBD

## Usage
btrfs_snaprotate is a command line tool. When invoked on a specific BTRFS subvolume, it
creates a directory in that subvolume (target directory) in which it creates a single snapshot.
The snapshot is named *label*_*timestamp*, where label is an ID that can be used to group
logical classes of snapshots together (for example daily, hourly, before_backup) and is user selecatble.
The timestamp is generated at second granularity by btrfs_snaprotate and appended to the label. The
timestamp has the format: YYYY-MM-DD_hh:mm:ss (MM - Month number, mm - minute). After a new snapshot has
been created, 

btrfs_snaprotate is invoked with the following command line options:

```
   btrfs_snaprotate [-l|--label=label] [-k|--keep=num] [-a|--after=command]
                    [-t|--target=dir] [-v] subvolume
```

 * `subvolume` - The subvolume to snapshot. This is the only mandatory argument.
 * `label` - The label attached to the snapshot name. If not specified, defaults to the last
             directory component of the subvolume.
 * `keep` - Number of snapshots to keep. After snapshot creation, btrfs_snaprotate will try
            to delete the oldest snapshot, such that no more than the specified number of snapshots
            remain. If the number of snapshots is equal or less than the specifed keep parameter,
            no snapshot will be deleted. This parameter only applies to snapshots that have a label
            identical to the label of the snapshot that was created.
 * `target` - A directory, located under the subvolume, that holds the created snapshot. If not specified,
              the default is `.snapshot`.
 * `after` - A command to run right after the creation of the new snapshot and the (optional) deletion
             of the old snapshots. The string passed to this argument is run under the system'
             default shell. It has the following environment variables defined:
   -  `SNAPSUBVOL` - The subvolume that was snapshot
   -  `SNAPTARGET` - The directory in which the snapshots are stored
   -  `SNAPRECENT` - The most recent snapshot

 * `v` - Increase log verbosity





