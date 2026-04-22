"""
Demo: GPT-SoVITS Voice Generation

Loads character voice settings from Character-voice-example folder
and generates speech for test sentences in English, Chinese, and Japanese.

Usage:
    python demo_gpt_sovits_voice.py
    
Requirements:
    - GPT-SoVITS API running at http://127.0.0.1:9880
    - Character-voice-example folder with voice settings
    - httpx: pip install httpx
"""

import asyncio
import json
import re
import shutil
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, Optional
import sys

try:
    import httpx
except ImportError:
    print("ERROR: httpx not installed. Run: pip install httpx")
    sys.exit(1)


# ============================================================================
# Data Models
# ============================================================================

@dataclass
class VoiceSettings:
    """Settings from voice_setting.txt"""
    gpt_weight: str
    sovits_weight: str
    default_ref_voice: str
    default_ref_setting: str
    gpt_type1: str
    gpt_type2: str


@dataclass
class RefAudioSettings:
    """Settings from reference audio config file"""
    speak_speed: float
    seconds_between_sentences: float
    top_k: int
    top_p: float
    temperature: float
    wav_file: str
    ref_text: str
    ref_language: str


# ============================================================================
# Configuration Parser
# ============================================================================

class ConfigParser:
    """Parse voice configuration files with key='value' format"""
    
    @staticmethod
    def parse_config(config_text: str) -> Dict[str, str]:
        """
        Parse configuration file in key='value' format.
        
        Example:
            SPEAK_SPEED=0.95
            REF_TEXT='うん、ノアちゃんは...'
            
        Returns dict with stripped quotes and converted values.
        """
        config = {}
        for line in config_text.strip().split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if '=' not in line:
                continue
            
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            
            # Remove surrounding quotes if present
            if (value.startswith("'") and value.endswith("'")) or \
               (value.startswith('"') and value.endswith('"')):
                value = value[1:-1]
            
            config[key] = value
        
        return config
    
    @staticmethod
    def load_voice_settings(voice_setting_path: Path) -> VoiceSettings:
        """Load voice_setting.txt and return VoiceSettings."""
        if not voice_setting_path.exists():
            raise FileNotFoundError(f"Voice settings not found: {voice_setting_path}")
        
        config = ConfigParser.parse_config(voice_setting_path.read_text(encoding='utf-8'))
        
        return VoiceSettings(
            gpt_weight=config['GPT_WEIGHT'],
            sovits_weight=config['SoVITS_WEIGHT'],
            default_ref_voice=config['DEFAULT_REF_VOICE'],
            default_ref_setting=config['DEFAULT_REF_SETTING'],
            gpt_type1=config['GPT_SOVITS_TYPE1'],
            gpt_type2=config['GPT_SOVITS_TYPE2'],
        )
    
    @staticmethod
    def load_ref_audio_settings(ref_setting_path: Path) -> RefAudioSettings:
        """Load reference audio settings file."""
        if not ref_setting_path.exists():
            raise FileNotFoundError(f"Reference settings not found: {ref_setting_path}")
        
        config = ConfigParser.parse_config(ref_setting_path.read_text(encoding='utf-8'))
        
        return RefAudioSettings(
            speak_speed=float(config['SPEAK_SPEED']),
            seconds_between_sentences=float(config['SECONDS_BETWEEN_SENTENCES']),
            top_k=int(config['TOP_K']),
            top_p=float(config['TOP_P']),
            temperature=float(config['TEMPERATURE']),
            wav_file=config['WAV_FILE'],
            ref_text=config['REF_TEXT'],
            ref_language=config['REF_LANGUAGE'],
        )


# ============================================================================
# GPT-SoVITS API Client
# ============================================================================

class GPTSoVITSClient:
    """Async HTTP client for GPT-SoVITS API"""
    
    def __init__(self, api_url: str = "http://127.0.0.1:9880"):
        self.api_url = api_url
        self.client = httpx.AsyncClient(timeout=120.0)
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()
    
    async def health_check(self) -> bool:
        """Check if GPT-SoVITS API is running"""
        try:
            response = await self.client.get(f"{self.api_url}/docs", follow_redirects=True)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return False
    
    async def set_gpt_weights(self, model_path: str) -> bool:
        """Load GPT model weights"""
        try:
            response = await self.client.post(
                f"{self.api_url}/set_gpt_weights",
                json={"weights_path": str(model_path)}
            )
            if response.status_code == 200:
                print(f"✓ GPT model loaded: {Path(model_path).name}")
                return True
            else:
                print(f"❌ Failed to load GPT model: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error setting GPT weights: {e}")
            return False
    
    async def set_sovits_weights(self, model_path: str) -> bool:
        """Load SoVITS model weights"""
        try:
            response = await self.client.post(
                f"{self.api_url}/set_sovits_weights",
                json={"weights_path": str(model_path)}
            )
            if response.status_code == 200:
                print(f"✓ SoVITS model loaded: {Path(model_path).name}")
                return True
            else:
                print(f"❌ Failed to load SoVITS model: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error setting SoVITS weights: {e}")
            return False
    
    async def generate_voice(
        self,
        text: str,
        ref_audio_path: str,
        ref_text: str,
        ref_language: str,
        text_language: str,
        speed_factor: float = 1.0,
        top_k: int = 5,
        top_p: float = 1.0,
        temperature: float = 1.0,
    ) -> Optional[bytes]:
        """
        Generate speech from text.
        
        Args:
            text: Text to synthesize
            ref_audio_path: Path to reference audio
            ref_text: Text corresponding to reference audio
            ref_language: Language of reference text (JA, ZH, EN, etc.)
            text_language: Language of input text
            speed_factor: Speech speed (0.5-2.0)
            top_k: Top-k sampling
            top_p: Top-p sampling
            temperature: Sampling temperature
            
        Returns:
            Audio bytes (WAV format) or None if failed
        """
        try:
            # Convert language codes to lowercase for API
            ref_lang_code = ref_language.lower() if ref_language.lower() in ['ja', 'zh', 'en', 'yue', 'ko'] else 'auto'
            text_lang_code = text_language.lower() if text_language.lower() in ['ja', 'zh', 'en', 'yue', 'ko'] else 'auto'
            
            payload = {
                "text": text,
                "text_lang": text_lang_code,
                "ref_audio_path": str(ref_audio_path),
                "prompt_text": ref_text,
                "prompt_lang": ref_lang_code,
                "speed_factor": speed_factor,
                "top_k": top_k,
                "top_p": top_p,
                "temperature": temperature,
                "text_split_method": "cut5",
                "media_type": "wav",
            }
            
            response = await self.client.post(
                f"{self.api_url}/tts",
                json=payload
            )
            
            if response.status_code == 200:
                return response.content
            else:
                print(f"❌ TTS generation failed: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error generating voice: {e}")
            return False


# ============================================================================
# Character Voice Manager
# ============================================================================

class CharacterVoiceManager:
    """Manage character voice generation"""
    
    def __init__(self, character_name: str, character_folder: Path, output_dir: Path):
        """
        Initialize character voice manager.
        
        Args:
            character_name: Character display name (e.g., "艾玛", "希罗")
            character_folder: Path to Character-voice-example/{character}/
            output_dir: Output directory for generated audio
        """
        self.character_name = character_name
        self.character_folder = character_folder
        self.output_dir = output_dir
        self.gpt_sovits_folder = character_folder / "GPT-SoVITS"
        
        # Load settings
        self.voice_settings = ConfigParser.load_voice_settings(
            self.gpt_sovits_folder / "voice_setting.txt"
        )
        
        # Load reference audio settings
        ref_setting_path = self.gpt_sovits_folder / self.voice_settings.default_ref_setting.lstrip('./')
        self.ref_audio_settings = ConfigParser.load_ref_audio_settings(ref_setting_path)
        
        # Resolve full paths
        self.gpt_model_path = self.gpt_sovits_folder / self.voice_settings.gpt_weight
        self.sovits_model_path = self.gpt_sovits_folder / self.voice_settings.sovits_weight
        self.ref_audio_path = self.gpt_sovits_folder / self.voice_settings.default_ref_voice.lstrip('./')
        
        # Create character output folder
        self.character_output_dir = output_dir / f"{character_name}"
        self.character_output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n{'='*70}")
        print(f"Character: {character_name}")
        print(f"{'='*70}")
        print(f"Folder: {character_folder}")
        print(f"GPT Model Type: {self.voice_settings.gpt_type2}")
        print(f"GPT Model: {self.voice_settings.gpt_weight}")
        print(f"SoVITS Model: {self.voice_settings.sovits_weight}")
        print(f"Reference Audio: {self.ref_audio_path.name}")
        print(f"Reference Text: {self.ref_audio_settings.ref_text[:60]}...")
        print(f"Speech Speed: {self.ref_audio_settings.speak_speed}")
    
    async def generate_speech(
        self,
        client: GPTSoVITSClient,
        text: str,
        language: str,
        output_filename: str,
    ) -> bool:
        """
        Generate speech for a text.
        
        Args:
            client: GPTSoVITSClient instance
            text: Text to synthesize
            language: Language code (EN, ZH, JA)
            output_filename: Output filename (e.g., "english.wav")
            
        Returns:
            True if successful, False otherwise
        """
        print(f"\n  📝 Text: {text}")
        print(f"  🌐 Language: {language}")
        
        audio_bytes = await client.generate_voice(
            text=text,
            ref_audio_path=str(self.ref_audio_path),
            ref_text=self.ref_audio_settings.ref_text,
            ref_language=self.ref_audio_settings.ref_language,
            text_language=language,
            speed_factor=self.ref_audio_settings.speak_speed,
            top_k=self.ref_audio_settings.top_k,
            top_p=self.ref_audio_settings.top_p,
            temperature=self.ref_audio_settings.temperature,
        )
        
        if audio_bytes:
            output_path = self.character_output_dir / output_filename
            output_path.write_bytes(audio_bytes)
            print(f"  ✓ Saved: {output_filename} ({len(audio_bytes)} bytes)")
            return True
        else:
            print(f"  ❌ Failed to generate speech")
            return False


# ============================================================================
# Main Demo
# ============================================================================

async def main():
    """Main demo function"""
    
    # Setup paths
    base_dir = Path(__file__).parent.parent
    character_voice_example = base_dir / "Character-voice-example"
    output_dir = base_dir / "dialogue-server" / "output" / "demo_voice"
    
    # Clean output directory
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "="*70)
    print("GPT-SoVITS Voice Generation Demo")
    print("="*70)
    
    # Initialize API client
    client = GPTSoVITSClient(api_url="http://127.0.0.1:9880")
    
    # Check API health
    print("\n🔍 Checking GPT-SoVITS API connection...")
    is_healthy = await client.health_check()
    if not is_healthy:
        print("❌ Cannot connect to GPT-SoVITS API at http://127.0.0.1:9880")
        print("   Please ensure GPT-SoVITS API is running:")
        print("   cd third_party/GPT-SoVITS-v2pro-20250604")
        print("   python api_v2.py -a 127.0.0.1 -p 9880")
        await client.close()
        return
    print("✓ GPT-SoVITS API is running")
    
    # Test sentences in multiple languages
    test_texts = [
        ("Good morning", "EN"),
        ("早上好", "ZH"),
        ("おはよう", "JA"),
    ]
    
    # Process characters
    characters = [
        ("艾玛", character_voice_example / "艾玛"),
        ("希罗", character_voice_example / "希罗"),
    ]
    
    for character_name, character_folder in characters:
        if not character_folder.exists():
            print(f"❌ Character folder not found: {character_folder}")
            continue
        
        manager = CharacterVoiceManager(character_name, character_folder, output_dir)
        
        # Load models
        print(f"\n📦 Loading models...")
        gpt_success = await client.set_gpt_weights(str(manager.gpt_model_path))
        sovits_success = await client.set_sovits_weights(str(manager.sovits_model_path))
        
        if not (gpt_success and sovits_success):
            print(f"❌ Failed to load models for {character_name}")
            continue
        
        # Generate speech for each test text
        print(f"\n🎤 Generating speech for {character_name}...")
        for text, language in test_texts:
            lang_name = {"EN": "English", "ZH": "Chinese", "JA": "Japanese"}[language]
            output_filename = f"{language.lower()}_{character_name}.wav"
            await manager.generate_speech(client, text, language, output_filename)
    
    await client.close()
    
    # Summary
    print(f"\n" + "="*70)
    print(f"✓ Demo completed!")
    print(f"📁 Output saved to: {output_dir}")
    print(f"="*70 + "\n")
    
    # List generated files
    if output_dir.exists():
        audio_files = list(output_dir.rglob("*.wav"))
        if audio_files:
            print("📋 Generated audio files:")
            for audio_file in sorted(audio_files):
                rel_path = audio_file.relative_to(output_dir)
                size_kb = audio_file.stat().st_size / 1024
                print(f"   - {rel_path} ({size_kb:.1f} KB)")
        else:
            print("⚠️  No audio files were generated.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
