package nospaceleft;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Scanner;


public class Main {
    static String INPUT_FILE = "input.txt";
    static final int TOTAL_DISK_SPACE = 70_000_000;
    static final int NEED_FREE_SPACE = 30_000_000;

    public static FsDirectory getRoot() {
        FsDirectory root = new FsDirectory("/", null);
        FsDirectory workingDir = root;

        File file = new File(Main.INPUT_FILE);
        try {
            Scanner scanner = new Scanner(file);
            while (scanner.hasNextLine()) {
                String line = scanner.nextLine();

                if (line.startsWith("$")) {
                    if (line.equals("$ cd ..")) {
                        workingDir = workingDir.parent;
                    } else if (line.equals("$ cd /")) {
                        workingDir = root;
                    } else if (line.startsWith("$ cd")) {
                        String[] args = line.split(" ");
                        if (workingDir.children.containsKey(args[2])) {
                            workingDir = (FsDirectory) workingDir.getChild(args[2]);
                        }
                    }
                    continue;
                }

                String[] args = line.split(" ");

                try {
                    int size = Integer.parseInt(args[0]);
                    String filename = args[1];
                    FsFile newFile = new FsFile(filename, size, workingDir);
                    workingDir.children.put(filename, newFile);
                } catch (NumberFormatException e) {
                    if (args[0].equals("dir") && !workingDir.hasChild(args[1])) {
                        FsDirectory new_dir = new FsDirectory(args[1], workingDir);
                        workingDir.addChild(args[1], new_dir);
                    }
                }
            }
            scanner.close();
        } catch(FileNotFoundException e)  {
            System.out.println("File Not Found: " + e.getLocalizedMessage());
            System.exit(1);
        }
        return root;
    }

    public static void main(String[] args) {
        if (args.length > 0) {
            Main.INPUT_FILE = args[0];
        }

        FsDirectory root = getRoot();
        int unusedSpace = TOTAL_DISK_SPACE - root.getSize();
        int leftToFree = NEED_FREE_SPACE - unusedSpace;
        FsDirectory dirToDelete = root;
        int dirToDeleteSize = dirToDelete.getSize();
        int sumPart1 = 0;

        Queue<FsDirectory> dirs = new LinkedList<>();
        dirs.add(root);
        while (!dirs.isEmpty()) {
            FsDirectory curDir = dirs.poll();
            int curDirSize = curDir.getSize();
            if (curDirSize <= 100_000) {
                sumPart1 += curDirSize;
            }

            if (curDirSize >= leftToFree && curDirSize < dirToDeleteSize) {
                dirToDelete = curDir;
                dirToDeleteSize = curDirSize;
            }

            for (FsItem child : curDir.children.values()) {
                if (child.isDirectory()) {
                    dirs.add((FsDirectory) child);
                }
            }

        }

        System.out.printf("ANSWER:\nPart 1: %d\nPart 2: %d (rm %s)", sumPart1, dirToDeleteSize, dirToDelete.fullPath());

    }
}
