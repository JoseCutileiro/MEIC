package pt.tecnico;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

import java.io.FileReader;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.io.IOException;

import java.io.File;
import java.util.Scanner;


import static javax.xml.bind.DatatypeConverter.printHexBinary;

import java.security.MessageDigest;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class SecureReader {
    public static void main(String[] args) throws IOException,Exception {
        // Check arguments
        if (args.length < 1) {
            System.err.println("Argument(s) missing!");
            System.err.printf("Usage: java %s file%n", JsonReader.class.getName());
            return;
        }
        final String filename = args[0];

        AESCipherByteArrayMixer cipher = new AESCipherByteArrayMixer(Cipher.DECRYPT_MODE);
        cipher.setParameters("keys/secret.key", "CBC");
        FileMixer.mix(args[0],"DecryptedDoc.json",cipher);

        // Read JSON object from file, and print its contets
        try (FileReader fileReader = new FileReader("DecryptedDoc.json")) {
            Gson gson = new Gson();
            JsonObject rootJson = gson.fromJson(fileReader, JsonObject.class);
            System.out.println("JSON object: " + rootJson);
            
            // FULL JSON: CHECK FOR INTEGRITY
            System.out.println("== plain text ==");
            System.out.println(rootJson.toString());

            System.out.println("== plain bytes ==");
            System.out.println(printHexBinary(rootJson.toString().getBytes()));
            byte[] plainBytes = rootJson.toString().getBytes();

            // INTEGRIDADE (Digest)
            final String DIGEST_ALGO = "SHA-256";
            MessageDigest messageDigest = MessageDigest.getInstance(DIGEST_ALGO);
            messageDigest.update(plainBytes);
            byte[] dgst = messageDigest.digest();

            System.out.println(" == Digest bytes == ");
            System.out.println(printHexBinary(dgst));
            
            File myObj = new File("jsonDigest.dgst");
            Scanner myReader = new Scanner(myObj);
            String data = myReader.nextLine();

            System.out.println("== dgst data ==");
            System.out.println(data);

            myReader.close();

            if (!printHexBinary(dgst).equals(data)) {
                System.out.println("document.json is compromised, INTEGRITY ABORT");
                return ;
            }
            else {
                System.out.println("document.json is not compromised, INTEGRITY SUCESS");
            }
            
            JsonObject headerObject = rootJson.get("header").getAsJsonObject();

            // FRESH CHECK TOKEN
            String receivedToken = rootJson.get("token").getAsString();

            File myToken = new File("fresh_token.txt");
            Scanner myTokenReader = new Scanner(myToken);
            String token = myTokenReader.nextLine();
            myTokenReader.close();

            if (Integer.parseInt(receivedToken) <= Integer.parseInt(token)) {
                System.out.println("Your document is not fresh, FRESHNESS ABORT");
                return ;
            }
            else {
                System.out.println("Your document is fresh, FRESHNESS SUCESS");

                // UPDATE TOKEN
                FileWriter fw = new FileWriter("fresh_token.txt");
                PrintWriter pw = new PrintWriter(fw);
                pw.print(receivedToken);
                pw.close();
            }

            System.out.println("Document header:");
            System.out.println("Titulo: " + headerObject.get("title").getAsString());
            System.out.println("Author: " + headerObject.get("author").getAsString());
            System.out.println("Version: " + headerObject.get("version").getAsInt());
            JsonArray tagsArray = headerObject.getAsJsonArray("tags");
            System.out.print("Tags: ");
            for (int i = 0; i < tagsArray.size(); i++) {
                System.out.print(tagsArray.get(i).getAsString());
                if (i < tagsArray.size() - 1) {
                    System.out.print(", ");
                } else {
                    System.out.println(); // Print a newline after the final tag
                }
            }
            System.out.println("Document status: " + rootJson.get("status").getAsString());
            System.out.println("Document body: " + rootJson.get("body").getAsString());
        }
    }
}
