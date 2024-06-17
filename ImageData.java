import java.nio.file.Path;
import java.nio.file.Paths;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Arrays;
import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;

public class ImageData {

    public static void main(String[] args) {
        String specificFolderPath = "./";
        processFolders(new File(specificFolderPath), specificFolderPath);
        postProcess(new File(specificFolderPath));
        
        String outputFilePath = "./imageData.txt";
        
        List<String> imageDataList = new ArrayList<>(); // Collect image data entries here

        try {
            Path basePath = Paths.get(specificFolderPath).toAbsolutePath().getParent();
            processFolders2(new File(specificFolderPath), imageDataList, basePath, "Finalized");
            Collections.sort(imageDataList); // Sort the list alphabetically
            writeToFile(outputFilePath, imageDataList); // Write the sorted list to the file
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void processFolders(File folder, String rootPath) {
        createReadme(folder, rootPath);
        File[] subDirs = folder.listFiles(File::isDirectory);
        if (subDirs != null) {
            for (File subDir : subDirs) {
                processFolders(subDir, rootPath);
            }
        }
    }

    private static void postProcess(File folder) {        
        File[] files = folder.listFiles();
        if (files != null) {
            for (File file : files) {
                if (file.isDirectory()) {
                    postProcess(file); // Recursively process subdirectories
                } else if (file.isFile() && file.getName().equalsIgnoreCase("README.md")) {
                    sortReadme(file); // Sort the README.md file
                }
            }
        }
    }

    private static void sortReadme(File readmeFile) {
        List<String> imageLines = new ArrayList<>();

        try (BufferedReader reader = new BufferedReader(new FileReader(readmeFile))) {
            String line;
            while ((line = reader.readLine()) != null) {
                if (line.startsWith("<")) {
                    imageLines.add(line);
                }
            }
            Collections.sort(imageLines, (a, b) -> {
                String aFilename = a.substring(a.indexOf(" /> ")).trim();
                String bFilename = b.substring(b.indexOf(" /> ")).trim();
                return aFilename.compareToIgnoreCase(bFilename);
            });
        } catch (IOException e) {
            e.printStackTrace();
        }

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(readmeFile))) {
            writer.write("# Image Previews\n\n");
            for (String imageLine : imageLines) {
                writer.write(imageLine);
                writer.write("\n\n");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void createReadme(File folder, String rootPath) {
        StringBuilder readmeContent = new StringBuilder("# Image Previews\n\n");
        generateImageLinks(folder, rootPath, folder.getAbsolutePath(), readmeContent, "");

        try (FileWriter writer = new FileWriter(new File(folder, "README.md"))) {
            writer.write(readmeContent.toString());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void generateImageLinks(File folder, String rootPath, String currentFolderPath, StringBuilder readmeContent, String relativePathPrefix) {
        File[] files = folder.listFiles();
        if (files != null) {
            for (File file : files) {
                if (file.isFile() && file.getName().endsWith(".png")) {
                    String relativeImagePath = relativePathPrefix + file.getName();
                    readmeContent.append(String.format("<img src=\"%s\" width=\"100\" /> %s<br>\n", relativeImagePath, file.getName()));
                } else if (file.isDirectory()) {
                    String newPrefix = relativePathPrefix + file.getName() + "/";
                    generateImageLinks(file, rootPath, currentFolderPath, readmeContent, newPrefix);
                }
            }
        }
    }

    private static void processFolders2(File folder, List<String> imageDataList, Path basePath, String rootFolderName) throws IOException {
        File[] files = folder.listFiles();
        if (files != null) {
            Arrays.sort(files, (f1, f2) -> f1.getName().compareToIgnoreCase(f2.getName()));

            for (File file : files) {
                if (file.isDirectory()) {
                    processFolders2(file, imageDataList, basePath, rootFolderName);
                } else if (file.isFile() && file.getName().endsWith(".png")) {
                    addImageInfoToList(file, imageDataList, basePath, rootFolderName);
                }
            }
        }
    }

    private static void addImageInfoToList(File file, List<String> imageDataList, Path basePath, String rootFolderName) throws IOException {
        BufferedImage image = ImageIO.read(file);
        if (image != null) {
            int width = image.getWidth();
            int height = image.getHeight();
            String relativePath = getRelativePath2(file, basePath, rootFolderName);
            String filenameWithoutExtension = file.getName().substring(0, file.getName().lastIndexOf('.'));
            imageDataList.add(String.format("%s %s %d %d", filenameWithoutExtension, relativePath, width, height));
        }
    }

    private static void writeToFile(String outputFilePath, List<String> imageDataList) throws IOException {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(outputFilePath))) {
            for (String line : imageDataList) {
                writer.write(line);
                writer.newLine();
            }
        }
    }

    private static String getRelativePath2(File file, Path basePath, String rootFolderName) {
        Path filePath = file.toPath().toAbsolutePath();
        String relativePath = basePath.relativize(filePath).toString().replace("\\", "/");
        return relativePath.replaceFirst("^" + rootFolderName + "/", "");
    }

    private static String getRelativePath(File file, String currentFolderPath) {
        Path filePath = file.toPath();
        Path folderPath = Paths.get(currentFolderPath);
        return folderPath.relativize(filePath).toString().replace("\\", "/");
    }
}
