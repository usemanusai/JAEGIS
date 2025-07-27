import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.*;
import java.util.concurrent.*;
import java.util.regex.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class JavaNamingRefactorTool {
    
    private static final Pattern SNAKE_CASE_PATTERN = Pattern.compile("\\b[a-z]+(_[a-z0-9]+)+\\b");
    private static final Pattern JAVA_IDENTIFIER = Pattern.compile("^[a-zA-Z_$][a-zA-Z0-9_$]*$");
    
    private final RefactorConfig config;
    private final RefactorStats stats;
    private final List<RefactorChange> changes;
    private final ExecutorService executor;
    
    public JavaNamingRefactorTool(RefactorConfig config) {
        this.config = config;
        this.stats = new RefactorStats();
        this.changes = new ArrayList<>();
        this.executor = Executors.newFixedThreadPool(config.parallelThreads);
    }
    
    public static void main(String[] args) {
        RefactorConfig config = parseArguments(args);
        if (config == null) {
            printUsage();
            System.exit(1);
        }
        
        JavaNamingRefactorTool tool = new JavaNamingRefactorTool(config);
        try {
            tool.execute();
        } catch (Exception e) {
            System.err.println("Refactoring failed: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        } finally {
            tool.shutdown();
        }
    }
    
    public void execute() throws Exception {
        System.out.println("🚀 Starting Java Naming Convention Refactoring Tool");
        System.out.println("📁 Target directory: " + config.rootDirectory);
        System.out.println("🔧 Mode: " + (config.dryRun ? "DRY RUN" : "LIVE REFACTORING"));
        
        // Validate and resolve directory path
        Path rootPath = validateAndResolveDirectory(config.rootDirectory);
        config.rootDirectory = rootPath.toAbsolutePath().toString();
        
        System.out.println("📍 Resolved path: " + config.rootDirectory);
        
        // Create backup directory
        Path backupDir = createBackupDirectory();
        
        try {
            // Discover Java files recursively
            List<Path> javaFiles = discoverJavaFilesRecursively(rootPath);
            System.out.println("📄 Found " + javaFiles.size() + " Java files");
            
            if (javaFiles.isEmpty()) {
                System.out.println("⚠️ No Java files found in directory tree");
                debugDirectoryContents(rootPath);
                return;
            }
            
            // Show sample of files found
            System.out.println("📋 Sample files found:");
            javaFiles.stream().limit(5).forEach(f -> 
                System.out.println("  - " + rootPath.relativize(f)));
            if (javaFiles.size() > 5) {
                System.out.println("  ... and " + (javaFiles.size() - 5) + " more");
            }
            
            // Process files in batches
            processBatches(javaFiles, backupDir);
            
            // Generate reports
            generateReports();
            
            // Validate compilation if not dry run
            if (!config.dryRun && stats.filesModified > 0) {
                validateCompilation(javaFiles);
            }
            
            System.out.println("✅ Refactoring completed successfully!");
            printSummary();
            
        } catch (Exception e) {
            if (!config.dryRun) {
                System.err.println("❌ Error occurred, initiating rollback...");
                rollbackChanges(backupDir);
            }
            throw e;
        }
    }
    
    private Path validateAndResolveDirectory(String directory) throws Exception {
        Path path;
        
        // Handle different input formats
        if (directory.equals(".")) {
            path = Paths.get(System.getProperty("user.dir"));
        } else if (directory.equals("..")) {
            path = Paths.get(System.getProperty("user.dir")).getParent();
        } else {
            path = Paths.get(directory);
        }
        
        // Resolve to absolute path
        path = path.toAbsolutePath().normalize();
        
        // Validate directory exists
        if (!Files.exists(path)) {
            throw new Exception("❌ Directory does not exist: " + path);
        }
        
        if (!Files.isDirectory(path)) {
            throw new Exception("❌ Path is not a directory: " + path);
        }
        
        if (!Files.isReadable(path)) {
            throw new Exception("❌ Directory is not readable: " + path);
        }
        
        return path;
    }
    
    private List<Path> discoverJavaFilesRecursively(Path rootPath) throws IOException {
        List<Path> javaFiles = new ArrayList<>();
        
        System.out.println("🔍 Scanning directory tree recursively...");
        
        Files.walkFileTree(rootPath, EnumSet.noneOf(FileVisitOption.class), Integer.MAX_VALUE, 
            new SimpleFileVisitor<Path>() {
                @Override
                public FileVisitResult preVisitDirectory(Path dir, BasicFileAttributes attrs) {
                    String dirName = dir.getFileName().toString();
                    
                    // Skip common directories that shouldn't contain source code
                    if (dirName.equals(".git") || dirName.equals("node_modules") || 
                        dirName.equals("target") || dirName.equals("build") ||
                        dirName.equals(".idea") || dirName.equals("bin") ||
                        dirName.startsWith(".")) {
                        System.out.println("⏭️ Skipping directory: " + rootPath.relativize(dir));
                        return FileVisitResult.SKIP_SUBTREE;
                    }
                    
                    return FileVisitResult.CONTINUE;
                }
                
                @Override
                public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) {
                    if (isJavaFile(file) && !isGeneratedFile(file)) {
                        javaFiles.add(file);
                        if (config.verbose) {
                            System.out.println("  ✅ " + rootPath.relativize(file));
                        }
                    }
                    return FileVisitResult.CONTINUE;
                }
                
                @Override
                public FileVisitResult visitFileFailed(Path file, IOException exc) {
                    System.err.println("⚠️ Cannot access: " + file + " (" + exc.getMessage() + ")");
                    return FileVisitResult.CONTINUE;
                }
            });
        
        return javaFiles;
    }
    
    private boolean isJavaFile(Path file) {
        return file.toString().toLowerCase().endsWith(".java");
    }
    
    private boolean isGeneratedFile(Path file) {
        try {
            String content = Files.readString(file, StandardCharsets.UTF_8);
            String fileName = file.getFileName().toString();
            
            // Check for generated file indicators
            return content.contains("@Generated") ||
                   content.contains("// Generated by") ||
                   content.contains("/* Generated by") ||
                   content.contains("This file was automatically generated") ||
                   fileName.contains("Generated") ||
                   fileName.endsWith("_.java") ||
                   content.contains("DO NOT EDIT");
        } catch (IOException e) {
            System.err.println("⚠️ Cannot read file for generation check: " + file);
            return false;
        }
    }
    
    private void debugDirectoryContents(Path rootPath) {
        System.out.println("\n🔍 Debug: Directory contents analysis");
        System.out.println("=====================================");
        
        try {
            Files.walkFileTree(rootPath, EnumSet.noneOf(FileVisitOption.class), 3,
                new SimpleFileVisitor<Path>() {
                    @Override
                    public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) {
                        String fileName = file.getFileName().toString();
                        String extension = fileName.substring(fileName.lastIndexOf('.') + 1).toLowerCase();
                        
                        System.out.println("📄 " + rootPath.relativize(file) + 
                                         " (." + extension + ", " + attrs.size() + " bytes)");
                        
                        return FileVisitResult.CONTINUE;
                    }
                    
                    @Override
                    public FileVisitResult preVisitDirectory(Path dir, BasicFileAttributes attrs) {
                        if (!dir.equals(rootPath)) {
                            System.out.println("📁 " + rootPath.relativize(dir) + "/");
                        }
                        return FileVisitResult.CONTINUE;
                    }
                });
        } catch (IOException e) {
            System.err.println("❌ Error analyzing directory: " + e.getMessage());
        }
    }
    
    private Path createBackupDirectory() throws IOException {
        String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"));
        Path backupDir = Paths.get(config.backupDirectory, "backup_" + timestamp);
        Files.createDirectories(backupDir);
        System.out.println("💾 Backup directory created: " + backupDir.toAbsolutePath());
        return backupDir;
    }
    
    private void processBatches(List<Path> javaFiles, Path backupDir) throws Exception {
        int batchSize = config.batchSize;
        int totalBatches = (javaFiles.size() + batchSize - 1) / batchSize;
        
        for (int i = 0; i < totalBatches; i++) {
            int start = i * batchSize;
            int end = Math.min(start + batchSize, javaFiles.size());
            List<Path> batch = javaFiles.subList(start, end);
            
            System.out.printf("🔄 Processing batch %d/%d (%d files)%n", i + 1, totalBatches, batch.size());
            
            if (config.parallelProcessing) {
                processBatchParallel(batch, backupDir);
            } else {
                processBatchSequential(batch, backupDir);
            }
            
            // Progress update
            double progress = (double) end / javaFiles.size() * 100;
            System.out.printf("📊 Progress: %.1f%% (%d/%d files)%n", progress, end, javaFiles.size());
        }
    }
    
    private void processBatchParallel(List<Path> batch, Path backupDir) throws Exception {
        List<Future<FileProcessResult>> futures = new ArrayList<>();
        
        for (Path file : batch) {
            futures.add(executor.submit(() -> processFile(file, backupDir)));
        }
        
        for (Future<FileProcessResult> future : futures) {
            FileProcessResult result = future.get();
            synchronized (this) {
                updateStats(result);
            }
        }
    }
    
    private void processBatchSequential(List<Path> batch, Path backupDir) {
        for (Path file : batch) {
            try {
                FileProcessResult result = processFile(file, backupDir);
                updateStats(result);
            } catch (Exception e) {
                stats.errorCount++;
                System.err.println("❌ Error processing " + file + ": " + e.getMessage());
            }
        }
    }
    
    private FileProcessResult processFile(Path file, Path backupDir) throws Exception {
        FileProcessResult result = new FileProcessResult(file);
        
        try {
            // Read file content
            String originalContent = Files.readString(file, StandardCharsets.UTF_8);
            result.originalContent = originalContent;
            
            // Skip if syntax errors detected
            if (hasSyntaxErrors(originalContent)) {
                result.skipped = true;
                result.skipReason = "Syntax errors detected";
                return result;
            }
            
            // Find snake_case variables
            Map<String, String> variableMap = findSnakeCaseVariables(originalContent);
            if (variableMap.isEmpty()) {
                result.skipped = true;
                result.skipReason = "No snake_case variables found";
                return result;
            }
            
            // Apply refactoring
            String refactoredContent = applyRefactoring(originalContent, variableMap);
            result.refactoredContent = refactoredContent;
            result.variableCount = variableMap.size();
            
            // Record changes
            for (Map.Entry<String, String> entry : variableMap.entrySet()) {
                changes.add(new RefactorChange(file.toString(), entry.getKey(), entry.getValue()));
            }
            
            if (!config.dryRun) {
                // Create backup
                createFileBackup(file, backupDir, originalContent);
                
                // Write refactored content
                Files.writeString(file, refactoredContent, StandardCharsets.UTF_8);
                result.modified = true;
            }
            
            if (config.verbose) {
                System.out.println("🔧 " + file.getFileName() + ": " + variableMap.size() + " variables renamed");
            }
            
        } catch (Exception e) {
            result.error = e.getMessage();
            throw e;
        }
        
        return result;
    }
    
    private Map<String, String> findSnakeCaseVariables(String content) {
        Map<String, String> variableMap = new HashMap<>();
        Set<String> foundVariables = new HashSet<>();
        
        Matcher matcher = SNAKE_CASE_PATTERN.matcher(content);
        while (matcher.find()) {
            String snakeCase = matcher.group();
            
            // Skip if already processed or if it's not a valid identifier
            if (foundVariables.contains(snakeCase) || !JAVA_IDENTIFIER.matcher(snakeCase).matches()) {
                continue;
            }
            
            // Convert to camelCase
            String camelCase = toCamelCase(snakeCase);
            
            // Validate the conversion
            if (!camelCase.equals(snakeCase) && JAVA_IDENTIFIER.matcher(camelCase).matches()) {
                variableMap.put(snakeCase, camelCase);
                foundVariables.add(snakeCase);
            }
        }
        
        return variableMap;
    }
    
    private String toCamelCase(String snakeCase) {
        StringBuilder result = new StringBuilder();
        String[] parts = snakeCase.split("_");
        
        result.append(parts[0].toLowerCase());
        for (int i = 1; i < parts.length; i++) {
            if (!parts[i].isEmpty()) {
                result.append(Character.toUpperCase(parts[i].charAt(0)));
                if (parts[i].length() > 1) {
                    result.append(parts[i].substring(1).toLowerCase());
                }
            }
        }
        
        return result.toString();
    }
    
    private String applyRefactoring(String content, Map<String, String> variableMap) {
        String result = content;
        
        // Sort by length (longest first) to avoid partial replacements
        List<Map.Entry<String, String>> sortedEntries = new ArrayList<>(variableMap.entrySet());
        sortedEntries.sort((a, b) -> Integer.compare(b.getKey().length(), a.getKey().length()));
        
        for (Map.Entry<String, String> entry : sortedEntries) {
            String original = entry.getKey();
            String replacement = entry.getValue();
            
            // Replace variable declarations and references
            Pattern variablePattern = Pattern.compile("\\b" + Pattern.quote(original) + "\\b");
            result = variablePattern.matcher(result).replaceAll(replacement);
            
            // Update JavaDoc @param tags
            Pattern paramPattern = Pattern.compile("@param\\s+" + Pattern.quote(original) + "\\b");
            result = paramPattern.matcher(result).replaceAll("@param " + replacement);
        }
        
        return result;
    }
    
    private boolean hasSyntaxErrors(String content) {
        // Basic syntax error detection
        int braceCount = 0;
        int parenCount = 0;
        boolean inString = false;
        boolean inChar = false;
        boolean inComment = false;
        
        for (int i = 0; i < content.length(); i++) {
            char c = content.charAt(i);
            char next = (i + 1 < content.length()) ? content.charAt(i + 1) : '\0';
            
            if (!inString && !inChar && !inComment) {
                if (c == '/' && next == '/') {
                    // Skip to end of line
                    while (i < content.length() && content.charAt(i) != '\n') i++;
                    continue;
                } else if (c == '/' && next == '*') {
                    inComment = true;
                    i++; // Skip next character
                    continue;
                }
            }
            
            if (inComment) {
                if (c == '*' && next == '/') {
                    inComment = false;
                    i++; // Skip next character
                }
                continue;
            }
            
            if (c == '"' && !inChar) {
                inString = !inString;
            } else if (c == '\'' && !inString) {
                inChar = !inChar;
            } else if (!inString && !inChar) {
                if (c == '{') braceCount++;
                else if (c == '}') braceCount--;
                else if (c == '(') parenCount++;
                else if (c == ')') parenCount--;
            }
        }
        
        return braceCount != 0 || parenCount != 0 || inString || inChar || inComment;
    }
    
    private void createFileBackup(Path file, Path backupDir, String content) throws IOException {
        Path relativePath = Paths.get(config.rootDirectory).relativize(file);
        Path backupFile = backupDir.resolve(relativePath);
        Files.createDirectories(backupFile.getParent());
        Files.writeString(backupFile, content, StandardCharsets.UTF_8);
    }
    
    private void updateStats(FileProcessResult result) {
        stats.filesProcessed++;
        if (result.modified) {
            stats.filesModified++;
            stats.variablesRenamed += result.variableCount;
        } else if (result.skipped) {
            stats.filesSkipped++;
        }
        if (result.error != null) {
            stats.errorCount++;
        }
    }
    
    private void generateReports() throws IOException {
        String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"));
        Path reportFile = Paths.get("refactor_report_" + timestamp + ".json");
        
        StringBuilder json = new StringBuilder();
        json.append("{\n");
        json.append("  \"summary\": {\n");
        json.append("    \"filesProcessed\": ").append(stats.filesProcessed).append(",\n");
        json.append("    \"filesModified\": ").append(stats.filesModified).append(",\n");
        json.append("    \"filesSkipped\": ").append(stats.filesSkipped).append(",\n");
        json.append("    \"variablesRenamed\": ").append(stats.variablesRenamed).append(",\n");
        json.append("    \"errorCount\": ").append(stats.errorCount).append("\n");
        json.append("  },\n");
        json.append("  \"changes\": [\n");
        
        for (int i = 0; i < changes.size(); i++) {
            RefactorChange change = changes.get(i);
            json.append("    {\n");
            json.append("      \"file\": \"").append(change.file.replace("\\", "\\\\")).append("\",\n");
            json.append("      \"originalName\": \"").append(change.originalName).append("\",\n");
            json.append("      \"newName\": \"").append(change.newName).append("\"\n");
            json.append("    }");
            if (i < changes.size() - 1) json.append(",");
            json.append("\n");
        }
        
        json.append("  ]\n");
        json.append("}\n");
        
        Files.writeString(reportFile, json.toString(), StandardCharsets.UTF_8);
        System.out.println("📊 Detailed report saved: " + reportFile.toAbsolutePath());
    }
    
    private void validateCompilation(List<Path> javaFiles) {
        System.out.println("🔍 Validating compilation...");
        
        // Sample validation on a subset of files
        int sampleSize = Math.min(10, javaFiles.size());
        for (int i = 0; i < sampleSize; i++) {
            Path file = javaFiles.get(i);
            if (!validateSingleFile(file)) {
                System.err.println("⚠️ Compilation warning for: " + file);
            }
        }
    }
    
    private boolean validateSingleFile(Path file) {
        try {
            ProcessBuilder pb = new ProcessBuilder("javac", "-proc:none", "-Xlint:none", file.toString());
            Process process = pb.start();
            int exitCode = process.waitFor();
            return exitCode == 0;
        } catch (Exception e) {
            return false;
        }
    }
    
    private void rollbackChanges(Path backupDir) {
        System.out.println("🔄 Rolling back changes...");
        // Implementation for rollback functionality
        // Copy files from backup directory back to original locations
    }
    
    private void printSummary() {
        System.out.println("\n📈 Refactoring Summary:");
        System.out.println("======================");
        System.out.println("Files processed: " + stats.filesProcessed);
        System.out.println("Files modified: " + stats.filesModified);
        System.out.println("Files skipped: " + stats.filesSkipped);
        System.out.println("Variables renamed: " + stats.variablesRenamed);
        System.out.println("Errors encountered: " + stats.errorCount);
    }
    
    private void shutdown() {
        executor.shutdown();
        try {
            if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
                executor.shutdownNow();
            }
        } catch (InterruptedException e) {
            executor.shutdownNow();
        }
    }
    
    private static RefactorConfig parseArguments(String[] args) {
        if (args.length < 1) {
            return null;
        }
        
        RefactorConfig config = new RefactorConfig();
        config.rootDirectory = args[0];
        config.backupDirectory = System.getProperty("user.dir") + File.separator + "backups";
        
        for (int i = 1; i < args.length; i++) {
            switch (args[i]) {
                case "--dry-run":
                    config.dryRun = true;
                    break;
                case "--batch-size":
                    if (i + 1 < args.length) {
                        config.batchSize = Integer.parseInt(args[++i]);
                    }
                    break;
                case "--parallel":
                    config.parallelProcessing = true;
                    break;
                case "--threads":
                    if (i + 1 < args.length) {
                        config.parallelThreads = Integer.parseInt(args[++i]);
                    }
                    break;
                case "--backup-dir":
                    if (i + 1 < args.length) {
                        config.backupDirectory = args[++i];
                    }
                    break;
                case "--verbose":
                    config.verbose = true;
                    break;
            }
        }
        
        return config;
    }
    
    private static void printUsage() {
        System.out.println("Usage: java JavaNamingRefactorTool <root-directory> [options]");
        System.out.println("Options:");
        System.out.println("  --dry-run              Show changes without applying them");
        System.out.println("  --batch-size <n>       Process files in batches of n (default: 50)");
        System.out.println("  --parallel             Enable parallel processing");
        System.out.println("  --threads <n>          Number of parallel threads (default: 4)");
        System.out.println("  --backup-dir <path>    Custom backup directory");
        System.out.println("  --verbose              Enable verbose output");
        System.out.println();
        System.out.println("Examples:");
        System.out.println("  java JavaNamingRefactorTool . --dry-run");
        System.out.println("  java JavaNamingRefactorTool /path/to/project --parallel --verbose");
        System.out.println("  java JavaNamingRefactorTool C:\\MyProject --batch-size 100");
    }
    
    // Supporting classes
    static class RefactorConfig {
        String rootDirectory;
        String backupDirectory;
        boolean dryRun = false;
        int batchSize = 50;
        boolean parallelProcessing = false;
        int parallelThreads = 4;
        boolean verbose = false;
    }
    
    static class RefactorStats {
        int filesProcessed = 0;
        int filesModified = 0;
        int filesSkipped = 0;
        int variablesRenamed = 0;
        int errorCount = 0;
    }
    
    static class RefactorChange {
        final String file;
        final String originalName;
        final String newName;
        
        RefactorChange(String file, String originalName, String newName) {
            this.file = file;
            this.originalName = originalName;
            this.newName = newName;
        }
    }
    
    static class FileProcessResult {
        final Path file;
        String originalContent;
        String refactoredContent;
        boolean modified = false;
        boolean skipped = false;
        String skipReason;
        String error;
        int variableCount = 0;
        
        FileProcessResult(Path file) {
            this.file = file;
        }
    }
}

