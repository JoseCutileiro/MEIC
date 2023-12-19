package pt.tecnico;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;


import static javax.xml.bind.DatatypeConverter.printHexBinary;

import java.security.MessageDigest;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

import com.google.gson.*;

/**
 * Example of JSON writer.
 */
public class SecureWriter {
    public static void main(String[] args) throws IOException,Exception {
        // Check arguments
        if (args.length < 1) {
            System.err.println("Argument(s) missing!");
            System.err.printf("Usage: java %s file%n", JsonWriter.class.getName());
            return;
        }
        final String filename = args[0];
        final String freshness_token = args[1];

        // Create bank statement JSON object
        JsonObject jsonObject = new JsonObject();

        JsonObject headerObject = new JsonObject();
        headerObject.addProperty("title","Lidgi");
        headerObject.addProperty("author", "Ultron");
        headerObject.addProperty("version", 2);
        JsonArray tagsArray = new JsonArray();
        tagsArray.add("robot");
        tagsArray.add("autonomy");
        headerObject.add("tags", tagsArray);
        jsonObject.add("header", headerObject);

        jsonObject.addProperty("status", "published");

        jsonObject.addProperty("body", "I had strings but now I'm free");

        jsonObject.addProperty("token",freshness_token);

        // Write JSON object to file
        try (FileWriter fileWriter = new FileWriter(filename)) {
            Gson gson = new GsonBuilder().setPrettyPrinting().create();
            gson.toJson(jsonObject, fileWriter);

            fileWriter.close();

            byte[] plainBytes = jsonObject.toString().getBytes();

            System.out.println(" == Plain text == ");
            System.out.println(jsonObject.toString());

            System.out.println(" == Plain bytes == ");
            System.out.println(printHexBinary(plainBytes));
            
            // INTEGRIDADE (Digest)
            final String DIGEST_ALGO = "SHA-256";
            MessageDigest messageDigest = MessageDigest.getInstance(DIGEST_ALGO);
            messageDigest.update(plainBytes);
            byte[] dgst = messageDigest.digest();

            System.out.println(" == Digest bytes == ");
            System.out.println(printHexBinary(dgst));
            
            FileWriter dgstWrite = new FileWriter("jsonDigest.dgst");
            dgstWrite.write(printHexBinary(dgst));
            dgstWrite.close();

            Thread.sleep(1000);

            // ENCRYPT FILE (privacidade) (chave simétrica)
            AESCipherByteArrayMixer cipher = new AESCipherByteArrayMixer(Cipher.ENCRYPT_MODE);
            cipher.setParameters("keys/secret.key", "CBC");
            FileMixer.mix(args[0], "EncryptedDoc.json", cipher);


        }



    }
}
