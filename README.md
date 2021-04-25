# ffmpeg-chapters

Generates chapter list in ffmpeg metadata format from simple csv-like input.  
For details see https://ffmpeg.org/ffmpeg-formats.html#Metadata-1

## Usage

`ffmpeg-chapters [FILE_LENGTH] <chapters`

Expects chapter list formatted like `HH:MM:SS;Chapter name` on stdin, one chapter per line, e.g. 

```
00:00:00;Chapter 1
00:45:13;Chapter 2
01:03:00;Chapter 3
```

`FILE_LENGTH` has `HH:MM:SS` format, just like the chapters.

If no file length specified as argument, last chapter will not have `END=` attribute.

## License

CC0. Might as well have been WTFPL, but this is better.

