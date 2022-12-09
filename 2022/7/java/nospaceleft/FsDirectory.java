package nospaceleft;

import java.util.*;

public class FsDirectory implements FsItem{
    public String name;
    public FsDirectory parent;
    public Map<String, FsItem> children;

    public FsDirectory(String name, FsDirectory parent) {
        this.name = name;
        this.parent = parent;
        this.children = new HashMap<>();
    }

    public int getSize() {
        int size = 0;
        for (FsItem item : this.children.values()) {
            size += item.getSize();
        }
        return size;
    }

    public boolean hasChild(String name) {
        return this.children.containsKey(name);
    }

    public FsItem getChild(String name) {
        return this.children.get(name);
    }

    public void addChild(String name, FsItem item) {
        this.children.put(name, item);
    }

    public boolean isDirectory() {
        return true;
    }

    public String fullPath() {
        if (this.parent == null) {
            return this.name;
        }
        StringBuilder sb = new StringBuilder();
        sb.append('/');
        List<FsDirectory> dirs = new LinkedList<>();
        FsDirectory par = this.parent;
        while (par.parent != null) {
            dirs.add(par);
            par = par.parent;
        }

        ListIterator<FsDirectory> li = dirs.listIterator(dirs.size());
        while (li.hasPrevious()) {
            sb.append(li.previous().name);
            sb.append('/');
        }
        sb.append(this.name);
        return sb.toString();
    }
}
