# Install ffmpeg
if ! command -v ffmpeg &> /dev/null; then
  echo "FFmpeg is not installed. Installing..."
  wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz
  wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz.md5
  md5sum -c ffmpeg-git-amd64-static.tar.xz.md5 > /dev/null
  tar xvf ffmpeg-git-amd64-static.tar.xz -C /tmp > /dev/null
  FFMPEG_DIR=$(find /tmp -type d -name "ffmpeg-git-*")
  sudo mv $FFMPEG_DIR/ffmpeg $FFMPEG_DIR/ffprobe /usr/local/bin/ > /dev/null
  echo "FFmpeg installed successfully."
else
  echo "FFmpeg is already installed. Skipping."
fi
