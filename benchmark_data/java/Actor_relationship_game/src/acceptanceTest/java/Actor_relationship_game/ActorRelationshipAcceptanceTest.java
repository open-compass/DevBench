package Actor_relationship_game;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertTrue;

public class ActorRelationshipAcceptanceTest {
    String referenceGraphPath;
    String referenceActorPath;
    String referenceFilePath;

    String testGraphPath;
    String testActorPath;
    String testFilePath;

    
    @BeforeEach
    public void setUp() {
        referenceGraphPath = "./src/acceptanceTest/java/Actor_relationship_game/actorGraph_reference.ser";
        referenceActorPath = "./src/acceptanceTest/java/Actor_relationship_game/actors_list_reference.txt";
        referenceFilePath = "./src/acceptanceTest/java/Actor_relationship_game/actor_connection_results_reference.txt";

        testGraphPath = "./src/acceptanceTest/java/Actor_relationship_game/actorGraph_test.ser";
        testActorPath = "./src/acceptanceTest/java/Actor_relationship_game/actors_list_test.txt";
        testFilePath = "./src/acceptanceTest/java/Actor_relationship_game/actor_connection_results_test.txt";
    }

    @AfterEach
    void tearDown() {
        // Clean up the test files
        new File(referenceGraphPath).delete();
        new File(referenceActorPath).delete();
        new File(referenceFilePath).delete();
        new File(testGraphPath).delete();
        new File(testActorPath).delete();
        new File(testFilePath).delete();
    }

    @Test
    public void testGeneratedFiles() throws IOException,InterruptedException{
        // tests
        runGradleTask("runGraphCreation -PfileName="+testGraphPath);
        runGradleTask("runActorGraphUtil -PgraphPath="+testGraphPath+" -PfilePath="+testActorPath);
        runGradleTask("runGameplayInterface -PgraphPath="+testGraphPath+" -PactorPath="+testActorPath+" -PfilePath="+testFilePath);

        File actorGraphTest= new File(testGraphPath);
        File actorListTest = new File(testActorPath);
        File resultTest = new File(testFilePath);

        assertTrue(actorGraphTest.exists(), "File actorGraph_test.ser should exist after graph creation.");
        assertTrue(actorListTest.exists(), "File actors_list_test.ser should exist after graph creation.");
        assertTrue(resultTest.exists(), "File actor_connection_results_test.ser should exist after graph creation.");
    }

    @Test
    public void testActorGraph() throws IOException,InterruptedException{
        runGradleTask("runGraphCreation -PfileName="+referenceGraphPath);
        runGradleTask("runGraphCreation -PfileName="+testGraphPath);

        File referenceActorGraph = new File(referenceGraphPath);
        File testActorGraph = new File(testGraphPath);
        byte[] reference = Files.readAllBytes(referenceActorGraph.toPath());
        byte[] test = Files.readAllBytes(testActorGraph.toPath());

        assertTrue(java.util.Arrays.equals(reference,test));
    }


    @Test
    public void testActorList() throws IOException,InterruptedException{
        runGradleTask("runGraphCreation -PfileName="+referenceGraphPath);
        runGradleTask("runGraphCreation -PfileName="+testGraphPath);
        runGradleTask("runActorGraphUtil -PgraphPath="+referenceGraphPath+" -PfilePath="+referenceActorPath);
        runGradleTask("runActorGraphUtil -PgraphPath="+testGraphPath+" -PfilePath="+testActorPath);


        List<String> referenceLines = Files.readAllLines(Paths.get(referenceActorPath));
        List<String> testLines = Files.readAllLines(Paths.get(testActorPath));

        for (String referenceLine:referenceLines){
            assertTrue(containsLine(testLines,referenceLine));
        }
    }

    @Test
    public void testConnectionResults() throws IOException, InterruptedException{
        runGradleTask("runGraphCreation -PfileName="+referenceGraphPath);
        runGradleTask("runGraphCreation -PfileName="+testGraphPath);
        runGradleTask("runActorGraphUtil -PgraphPath="+referenceGraphPath+" -PfilePath="+referenceActorPath);
        runGradleTask("runActorGraphUtil -PgraphPath="+testGraphPath+" -PfilePath="+testActorPath);
        runGradleTask("runGameplayInterface -PgraphPath="+referenceGraphPath+" -PactorPath="+referenceActorPath+" -PfilePath="+referenceFilePath);
        runGradleTask("runGameplayInterface -PgraphPath="+testGraphPath+" -PactorPath="+testActorPath+" -PfilePath="+testFilePath);


        BufferedReader referenceFile = new BufferedReader(new FileReader(referenceFilePath));
        List<String> testLines = Files.readAllLines(Paths.get(testFilePath));

        String referenceline;
        while ((referenceline=referenceFile.readLine())!=null){
            if (referenceline.contains("Connection Number")){
                assertTrue(containsLine(testLines,referenceline));
            }
        }
    }

    private boolean containsLine(List<String> outputLines, String expectedLine) {
        return outputLines.stream().anyMatch(line -> line.trim().equals(expectedLine));
    }



    private void runGradleTask(String taskName) throws IOException, InterruptedException {
        ProcessBuilder builder = new ProcessBuilder();
        if (System.getProperty("os.name").toLowerCase().startsWith("windows")) {
            builder.command("cmd", "/c", "gradlew " + taskName);
        } else {
            builder.command("sh", "-c", "./gradlew " + taskName);
        }
        builder.directory(new java.io.File("."));
        Process process = builder.start();

        // Capture and log the output
        BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
        String line;
        while ((line = reader.readLine()) != null) {
            System.out.println(line);
        }

        // Check for and handle errors
        BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
        while ((line = errorReader.readLine()) != null) {
            System.err.println(line);
        }

        int exitCode = process.waitFor();
        if (exitCode != 0) {
            throw new RuntimeException("Gradle task failed with exit code " + exitCode);
        }
    }

}
