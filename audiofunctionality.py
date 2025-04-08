import yt_dlp
import discord
import asyncio

async def main(message):
    # Connect to the voice channel
    voice_channel = message.author.voice.channel;
    voice_client = message.guild.voice_client;
    
    if not voice_client:
        voice_client = await voice_channel.connect();
        await asyncio.sleep(1);  # Ensure bot has connected to the channel
        await message.channel.send("Joined voice channel");
    
    elif voice_client.channel != voice_channel:
        await voice_channel.connect();
        await asyncio.sleep(1);
        await message.channel.send("Joined the correct voice channel");

    await message.channel.send("🎵 Launching music player...");

    # Stop current audio if any
    if voice_client.is_playing():
        voice_client.stop();

    # Check if voice client is ready to play
    if not voice_client.is_connected():
        await message.channel.send("Failed to connect to voice channel.");
        return;

    # YouTube link to play (test with a short song)
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ";

    # Download audio URL from YouTube
    ydl_opts = {
        'format': 'bestaudio',
        'quiet': True,
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False);
            audio_url = info['url'];
            title = info.get('title', 'Unknown Title');
    except Exception as e:
        await message.channel.send(f"Error extracting audio: {e}");
        return;

    # Create audio source with ffmpeg
    try:
        audio_source = await discord.FFmpegOpusAudio.from_probe(audio_url);
    except Exception as e:
        await message.channel.send(f"Error creating audio source: {e}");
        return;

    # Play audio
    voice_client.play(audio_source);
    await message.channel.send(f"🎶 Now playing: **{title}**");