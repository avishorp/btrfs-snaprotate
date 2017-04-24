#!/bin/sh

BASE=/testdisk

# Make sure the base dir is a btrfs volume
if [ ! `stat --format=%i $BASE` -eq 256 ]
then
  echo $BASE is not a BTRFS volume, aborting
  exit 1 
fi

T=$BASE/s
DUT=./btrfs_snaprotate
TARGET=aaaa

btrfs subvolume create $T


echo "*** Create first snapshot"
echo "hello" > $T/file1
sleep 2
$DUT --keep 4 --target $TARGET -v $T

echo "*** Create 2nd snapshot"
echo "hello" > $T/file2
sleep 2
$DUT --keep 4 --target $TARGET -v $T

echo "*** Create 3rd snapshot"
echo "hello" > $T/file3
sleep 2
$DUT --keep 4 --target $TARGET -v $T

echo "*** Create 4th snapshot"
echo "hello" > $T/file4
sleep 2
$DUT --keep 4 --target $TARGET -v $T

echo "*** Create 5th snapshot"
echo "hello" > $T/file5
sleep 2
$DUT --keep 4 --target $TARGET  -v $T

echo "*** Create 6th snapshot"
echo "hello" > $T/file6
sleep 2
$DUT --keep 4 --target $TARGET -v $T

echo "*** Listing snapshot directory, expect 4 recent ones"
ls /testdisk/s/$TARGET

# Cleanup
btrfs subvolume list -o /testdisk/s | awk -v T=$BASE '{ print T "/" $9 }'  | xargs btrfs subvolume delete
btrfs subvolume delete /testdisk/s
