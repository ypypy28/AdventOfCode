package nospaceleft;

import java.util.List;
import java.util.LinkedList;
import java.util.ListIterator;

public class FsFile implements FsItem{

    public int size;
    public String name;
    public FsDirectory parent;

    public FsFile(String name, int size, FsDirectory parent) {
        this.name = name;
        this.size = size;
        this.parent = parent;
    }
    public int getSize() {
        return size;
    }

    public boolean isDirectory() {
        return false;
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
