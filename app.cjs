let { NodeIO } = require("@gltf-transform/core");
let {
  prune,
  dedup,
  resample,
  textureResize,
  instance,
  textureCompress,
} = require("@gltf-transform/functions");
let sharp = require("sharp");

let extensions = require("@gltf-transform/extensions");
const express = require("express");
const app = express();
const port = 3001;

let draco3d = require("draco3dgltf");

// app.use(express.json({ limit: "1GB" })); // for parsing application/json

app.use(
  express.raw({
    limit: "1GB",
  })
);
app.post("/file", async (req, res) => {
  try {
    const io = new NodeIO();

    io.registerExtensions(extensions.ALL_EXTENSIONS);
    io.registerDependencies({
      "draco3d.decoder": await draco3d.createDecoderModule(), // Optional.
      "draco3d.encoder": await draco3d.createEncoderModule(), // Optional.
    });

    let document;

    let data = req.body;

    document = await io.readBinary(data); // Uint8Array → Document

    // Write.
    // await io.write("model.glb", document); // → void

    await document.transform(
      // Remove duplicate vertex or texture data, if any.
      dedup(),

      instance(),

      // Losslessly resample animation frames.
      resample(),

      // Remove unused nodes, textures, or other data.
      prune(),

      // Resize all textures to ≤1K.
      textureResize({ size: [1024, 1024] }),

      textureCompress({
        encoder: sharp,
        targetFormat: "webp",
        slots: /^(?!normalTexture).*$/, // exclude normal maps
      })
    );

    document
      .createExtension(extensions.KHRDracoMeshCompression)
      .setRequired(true)
      .setEncoderOptions({
        method: extensions.KHRDracoMeshCompression.EncoderMethod.EDGEBREAKER,
        encodeSpeed: 5,
        decodeSpeed: 5,
      });

    const glb = await io.writeBinary(document); // Document → Uint8Array

    console.log(glb);

    await io.write(`./out/export-${new Date().getTime()}.glb`, document);

    res.json({ ok: true });
  } catch (e) {
    console.log(e);

    res.json({ error: true });
  }
});

app.listen(port, () => {
  console.log(`Port ${port}`);
});
