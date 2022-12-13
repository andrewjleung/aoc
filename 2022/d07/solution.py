from dataclasses import dataclass, field
import os

"""
PART 1

You are given a filesystem that consists of a tree of files (plain data) and 
directories which may be further nested. The outermost directory is `/`.

You are also given a list of command-line output, where lines which start with
`$` are commands which may include `cd` or `ls`. 

`cd` lets you move into a specified directory (one level) or back out one level.
`ls` then will print all the files/directories in the following format:

- File:      `<size> <name>`
- Directory: `dir <name>`

Based upon this file input, find all directories with a total size at most 
100000 then calculate the sum of their total sizes.

Starting off, we want to construct the file tree from the input.
"""


"""
There should be two stages to this:
- Construction: parsing input to create the file tree.
- Answering:    traversing the tree recursively to determine file sizes. 

The parsing strategy goes:
- Maintain state of a stack of directories representing the path from the base
  directory to the current working directory.
- Parse commands until the entire input is parsed.
- To parse a command, determine what type of command it is then parse all the
  lines of that command.
- To parse a `cd` command, append the requested directory to the path, creating
  the directory if it doesn't exist in the current working directory.  
- To parse an `ls` command, parse and create files and directories within the
  current working directory until all have been parsed.
  

To then answer the question, we need to sum up the sizes of each directory, 
accumulating any sizes which are less than or equal to 100000.

We can do this by recursively navigating through the file tree. Getting the size
of a file is just returning its size. Files in this way are our leaves. Getting
the size of a directory on the other hand involves summing the sizes of all of
its contents.

When finding the size of a directory, afterwards we want to verify its size and,
if it is less than or equal to 100000, accumulate it.
"""


@dataclass
class File:
    size: int


@dataclass
class Directory:
    files: dict[str, File] = field(default_factory=dict)
    directories: dict[str, "Directory"] = field(default_factory=dict)


def isCd(line: str) -> bool:
    return line.startswith("$ cd")


def isLs(line: str) -> bool:
    return line == "$ ls"


def parseCd(
    lines: list[str], i: int, location: list[Directory]
) -> tuple[int, list[Directory]]:
    line = lines[i]
    destination = line.split(" ")[-1]

    if destination == "..":
        location.pop()
        return (i + 1, location)

    if destination == "/":
        return (i + 1, location[:1])

    # Move into the requested directory, creating it if it doesn't exist.
    cwd = location[-1]
    cwd.directories[destination] = cwd.directories.get(destination, Directory())
    location.append(cwd.directories[destination])
    return (i + 1, location)


def isDirectory(line: str) -> bool:
    return line.startswith("dir")


def isFile(line: str) -> bool:
    return not line.startswith("$") and not isDirectory(line)


def parseDirectory(line: str, location: list[Directory]):
    name = line.split(" ")[1]
    print(location)
    cwd = location[-1]
    cwd.directories[name] = Directory()


def parseFile(line: str, location: list[Directory]):
    tokens = line.split(" ")
    size = int(tokens[0])
    name = tokens[1]
    cwd = location[-1]
    cwd.files[name] = File(size)


def parseLs(
    lines: list[str], i: int, location: list[Directory]
) -> tuple[int, list[Directory]]:
    i += 1

    while i < len(lines):
        line = lines[i]

        if isDirectory(lines[i]):
            parseDirectory(line, location)
            i += 1
        elif isFile(lines[i]):
            parseFile(line, location)
            i += 1
        else:
            break

    return (i, location)


def parseCommand(
    lines: list[str], i: int, location: list[Directory]
) -> tuple[int, list[Directory]]:
    if isCd(lines[i]):
        return parseCd(lines, i, location)
    elif isLs(lines[i]):
        return parseLs(lines, i, location)
    else:
        raise ValueError(f"Unrecognized command: {lines[i]}")


fileDir = os.path.dirname(os.path.realpath("__file__"))


def getAbsolutePath(filename: str):
    return os.path.join(fileDir, "2022/d07", filename)


def readInput(filename: str) -> Directory:
    filesystem = Directory()
    location = [filesystem]

    with open(getAbsolutePath(filename)) as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        i = 0

        while i < len(lines):
            i, location = parseCommand(lines, i, location)

    return filesystem


SMALL_SIZE_THRESHOLD = 100000
DISK_SPACE = 70000000
UPDATE_SIZE = 30000000


def getDirectorySizes(filesystem: "Directory") -> int:
    directorySizes = []

    def getDirectorySize(dir: "Directory") -> int:
        nonlocal directorySizes

        directoriesSizeSum = sum(
            [getDirectorySize(d) for d in dir.directories.values()]
        )
        filesSizeSum = sum([f.size for f in dir.files.values()])
        total = directoriesSizeSum + filesSizeSum

        directorySizes.append(total)
        return total

    getDirectorySize(filesystem)
    return directorySizes


def sumSmallDirectorySizes(filesystem: "Directory") -> int:
    return sum(
        [size for size in getDirectorySizes(filesystem) if size <= SMALL_SIZE_THRESHOLD]
    )


def getSmallestDirectorySizeToDelete(filesystem: "Directory") -> int:
    sizes = getDirectorySizes(filesystem)
    filesystemSize = sizes[-1]

    spaceLeft = DISK_SPACE - filesystemSize
    spaceRequiredForUpdate = UPDATE_SIZE - spaceLeft

    # Find the smallest directory which is greater than the space required for
    # the update.
    return min([size for size in sizes if size >= spaceRequiredForUpdate])
