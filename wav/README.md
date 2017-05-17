# Wavs para generar difonos

- `normal.wav` es la palabra normalizadora. Grabarla con `arecord -f S16 -r 16000 normal.wav`

## Palabras:

Para grabar las palabras y escuchar la palabra normalizadora, usar el siguiente comando

```bash
$ WAV_NAME=word_name.wav; play normal.wav && arecord -f S16 -r 16000 $WAV_NAME && play normal.wav $WAV_NAME
```

Reemplazar `word_name.wav` por el nombre de la palabra en cuestión.
