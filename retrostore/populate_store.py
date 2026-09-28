import os
import django
from django.core.files.base import ContentFile
import urllib.request

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'retrostore.settings')
django.setup()

from store.models import Product

# Enlaces ultra estables al repositorio oficial de escaneos de cajas de Libretro/RetroArch
game_box_arts = {
    "Super Mario Bros (NES)": "https://raw.githubusercontent.com/libretro-thumbnails/Nintendo_-_Nintendo_Entertainment_System/master/Named_Boxarts/Super%20Mario%20Bros.%20(World).png",
    "The Legend of Zelda (NES)": "https://raw.githubusercontent.com/libretro-thumbnails/Nintendo_-_Nintendo_Entertainment_System/master/Named_Boxarts/Legend%20of%20Zelda%2C%20The%20(USA).png",
    "Sonic the Hedgehog (Genesis)": "https://raw.githubusercontent.com/libretro-thumbnails/Sega_-_Mega_Drive_-_Genesis/master/Named_Boxarts/Sonic%20The%20Hedgehog%20(USA%2C%20Europe).png",
    "Street Fighter II (Arcade)": "https://raw.githubusercontent.com/libretro-thumbnails/Sega_-_Mega_Drive_-_Genesis/master/Named_Boxarts/Street%20Fighter%20II'%20-%20Special%20Champion%20Edition%20(USA).png",
    "Pac-Man (Arcade)": "https://raw.githubusercontent.com/libretro-thumbnails/Nintendo_-_Nintendo_Entertainment_System/master/Named_Boxarts/Pac-Man%20(USA)%20(Namco).png",
    "Tetris (Game Boy)": "https://raw.githubusercontent.com/libretro-thumbnails/Nintendo_-_Game_Boy/master/Named_Boxarts/Tetris%20(World).png",
    "Metroid (NES)": "https://raw.githubusercontent.com/libretro-thumbnails/Nintendo_-_Nintendo_Entertainment_System/master/Named_Boxarts/Metroid%20(USA).png",
    "Chrono Trigger (SNES)": "https://raw.githubusercontent.com/libretro-thumbnails/Nintendo_-_Super_Nintendo_Entertainment_System/master/Named_Boxarts/Chrono%20Trigger%20(USA).png",
    "Donkey Kong Country (SNES)": "https://raw.githubusercontent.com/libretro-thumbnails/Nintendo_-_Super_Nintendo_Entertainment_System/master/Named_Boxarts/Donkey%20Kong%20Country%20(USA).png",
    "Mega Man 2 (NES)": "https://raw.githubusercontent.com/libretro-thumbnails/Nintendo_-_Nintendo_Entertainment_System/master/Named_Boxarts/Mega%20Man%202%20(USA).png",
    "Castlevania (NES)": "https://raw.githubusercontent.com/libretro-thumbnails/Nintendo_-_Nintendo_Entertainment_System/master/Named_Boxarts/Castlevania%20(USA).png",
    "Final Fantasy VII (PS1)": "https://raw.githubusercontent.com/libretro-thumbnails/Sony_-_PlayStation/master/Named_Boxarts/Final%20Fantasy%20VII%20(USA).png",
    "Street Fighter Alpha 3 (Arcade)": "https://raw.githubusercontent.com/libretro-thumbnails/Sony_-_PlayStation/master/Named_Boxarts/Street%20Fighter%20Alpha%203%20(USA).png",
    "GoldenEye 007 (N64)": "https://raw.githubusercontent.com/libretro-thumbnails/Nintendo_-_Nintendo_64/master/Named_Boxarts/GoldenEye%20007%20(USA).png",
    "Pokemon Red (Game Boy)": "https://raw.githubusercontent.com/libretro-thumbnails/Nintendo_-_Game_Boy/master/Named_Boxarts/Pokemon%20-%20Red%20Version%20(USA%2C%20Europe).png",
    "Resident Evil (PS1)": "https://raw.githubusercontent.com/libretro-thumbnails/Sony_-_PlayStation/master/Named_Boxarts/Resident%20Evil%20(USA).png",
    "Mortal Kombat II (Arcade)": "https://raw.githubusercontent.com/libretro-thumbnails/Sega_-_Mega_Drive_-_Genesis/master/Named_Boxarts/Mortal%20Kombat%20II%20(World).png",
    "Doom (PC)": "https://raw.githubusercontent.com/libretro-thumbnails/Sony_-_PlayStation/master/Named_Boxarts/Doom%20(USA).png",
    "Contra (NES)": "https://raw.githubusercontent.com/libretro-thumbnails/Nintendo_-_Nintendo_Entertainment_System/master/Named_Boxarts/Contra%20(USA).png",
    "Crash Bandicoot (PS1)": "https://raw.githubusercontent.com/libretro-thumbnails/Sony_-_PlayStation/master/Named_Boxarts/Crash%20Bandicoot%20(USA).png",
}

games = [
    ("Super Mario Bros (NES)", "El clásico de plataformas de 1985 que definió una era dorada.", 29.99, 15),
    ("The Legend of Zelda (NES)", "Comienza la legendaria aventura de Link explorando calabozos en Hyrule.", 34.99, 10),
    ("Sonic the Hedgehog (Genesis)", "Velocidad supersónica, anillos y plataformas inolvidables de SEGA.", 24.99, 12),
    ("Street Fighter II (Arcade)", "El juego de lucha definitivo de los 90s con combos y poderes icónicos.", 39.99, 8),
    ("Pac-Man (Arcade)", "Come puntos, esquiva y persigue fantasmas en este laberinto neón.", 19.99, 20),
    ("Tetris (Game Boy)", "El puzzle perfecto, adictivo y atemporal que conquistó el mundo.", 14.99, 25),
    ("Metroid (NES)", "Explora el misterioso planeta Zebes con la cazarrecompensas Samus Aran.", 29.99, 7),
    ("Chrono Trigger (SNES)", "Una obra maestra absoluta de los RPGs clásicos de viajes temporales.", 49.99, 5),
    ("Donkey Kong Country (SNES)", "Gráficos prerenderizados y música legendaria en la selva.", 32.99, 9),
    ("Mega Man 2 (NES)", "Derrota a los 8 Robot Masters en este desafiante plataformas de acción.", 27.99, 14),
    ("Castlevania (NES)", "Enfréntate al Conde Drácula con el icónico látigo Vampire Killer.", 28.99, 11),
    ("Final Fantasy VII (PS1)", "La épica aventura cinemática de Cloud Strife contra Shinra.", 45.99, 6),
    ("Street Fighter Alpha 3 (Arcade)", "Evolución total del combate arcade con múltiples estilos de lucha.", 35.99, 8),
    ("GoldenEye 007 (N64)", "El pionero del multijugador en primera persona para consolas.", 39.99, 4),
    ("Pokemon Red (Game Boy)", "Atrapa, entrena e intercambia a los 151 monstruos de bolsillo iniciales.", 29.99, 18),
    ("Resident Evil (PS1)", "Terror de supervivencia clásico atrapados en la tenebrosa mansión Spencer.", 36.99, 7),
    ("Mortal Kombat II (Arcade)", "Fatalities mejorados, sangre y peleas salvajes en salones arcade.", 33.99, 10),
    ("Doom (PC)", "Acción frenética de disparos en primera persona contra hordas del infierno.", 22.99, 20),
    ("Contra (NES)", "Disparos y acción cooperativa extrema con el famoso código Konami.", 21.99, 15),
    ("Crash Bandicoot (PS1)", "El carismático marsupial saltando cajas y frutas Wumpa en la isla.", 29.99, 12),
]

print(">>> Descargando portadas oficiales desde Libretro GitHub...")
for name, desc, price, stock in games:
    product, created = Product.objects.get_or_create(
        name=name,
        defaults={
            'description': desc,
            'price': price,
            'stock': stock
        }
    )
    product.stock = stock
    product.price = price
    product.save()

    img_url = game_box_arts.get(name)
    if img_url:
        try:
            req = urllib.request.Request(
                img_url, 
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req) as response:
                file_content = ContentFile(response.read())
                file_name = f"{name.lower().replace(' ', '_').replace('(', '').replace(')', '')}.png"
                product.image.save(file_name, file_content, save=True)
                print(f"[OK] Portada guardada: {name}")
        except Exception as e:
            print(f"[ERROR CRÍTICO] {name}: {e}")

print(">>> ¡Finalizado! Las portadas reales de colección están listas.")