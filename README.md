# Instrucciones

Usar con Python 2.7.13 + pip + praat 6.0.29

1. Instalar dependencias

```
$ sudo apt-get install ffmpeg
$ pip install -r requirements.txt
```

2. Correr

```
$ python tts.py kakasakapApa? kaka.wav
```


# Cómo modificamos el pitch en las preguntas


En base a observaciones hechas sobre grabaciones nuestras, decidimos agregar un "pico" en el pitch sobre el final de la palabra.

Para hacer esto, utilizamos una función cuadrática que comienza en la antepenúltima sílaba y que incrementa (en su valor máximo) en un factor de 0.35 el promedio del pitch del hablante. Por ejemplo, si el promedio del pitch del hablante es de 100hz, incrementará hasta en 35hz su pitch durante la anteúltima sílaba, y luego descenderá hasta casi su nivel normal.

Todo esto está implementado en el módulo `utils.questionify` y en la función `_find_peak_limits` de `tts`, con sus respectivos comentarios.

