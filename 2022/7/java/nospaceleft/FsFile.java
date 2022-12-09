package nospaceleft;

public class FsFile implements FsItem{

    public int size;
    public String name;

    public FsFile(String name, int size) {
        this.name = name;
        this.size = size;
    }
    public int getSize() {
        return size;
    }

    public boolean isDirectory() {
        return false;
    }
}
