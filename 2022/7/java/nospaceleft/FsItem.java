package nospaceleft;

public interface FsItem {
    public int getSize();
    public boolean isDirectory();
    public String fullPath();
}
