from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Caminhos para imagens de referência
reference_images = [
  {"local": "Green Island", "path": BASE_DIR / "assets/map101.png"},
  {"local": "Wildwind Island", "path": BASE_DIR / "assets/map102.png"},
  {"local": "Wildwind Island", "path": BASE_DIR / "assets/map103.png"},
  {"local": "Saffron", "path": BASE_DIR / "assets/map104.png"},
  {"local": "Hurricane Island", "path": BASE_DIR / "assets/map105.png"},
  {"local": "Shell Island", "path": BASE_DIR / "assets/map106.png"},
  {"local": "Shell Island", "path": BASE_DIR / "assets/map107.png"},
  {"local": "Shell Island", "path": BASE_DIR / "assets/map108.png"},
  {"local": "Tropical Island", "path": BASE_DIR / "assets/map109.png"},
  {"local": "Tropical Island", "path": BASE_DIR / "assets/map110.png"},
  {"local": "Tropical Island", "path": BASE_DIR / "assets/map111.png"},
  {"local": "Power Plant", "path": BASE_DIR / "assets/map112.png"},
  {"local": "Tropical Island", "path": BASE_DIR / "assets/map113.png"},
  {"local": "Dark Light Island", "path": BASE_DIR / "assets/map114.png"},
  {"local": "Pinkan Island", "path": BASE_DIR / "assets/map115.png"},
  {"local": "Tarroco Island", "path": BASE_DIR / "assets/map116.png"},
  {"local": "Valencia Island", "path": BASE_DIR / "assets/map117.png"},
  {"local": "Kabuto Fossil Island", "path": BASE_DIR / "assets/map118.png"},
  {"local": "Old Village (Aipom)", "path": BASE_DIR / "assets/map119.png"},
  {"local": "Seafoam Island (Castform)", "path": BASE_DIR / "assets/map120.png"},
  {"local": "Cleopatra Island", "path": BASE_DIR / "assets/map121.png"},
  {"local": "Sphinx Island", "path": BASE_DIR / "assets/map122.png"},
  {"local": "Kinnow Island", "path": BASE_DIR / "assets/map123.png"},
  {"local": "Dark Moon Island", "path": BASE_DIR / "assets/map124.png"},
  {"local": "Kinnow Island", "path": BASE_DIR / "assets/map125.png"},
  {"local": "Golden Island", "path": BASE_DIR / "assets/map126.png"},
  {"local": "Kinnow Island", "path": BASE_DIR / "assets/map127.png"}, 
  {"local": "Kinnow Island", "path": BASE_DIR / "assets/map128.png"},
  {"local": "Saffron", "path": BASE_DIR / "assets/map407.png"},
  {"local": "Fairchild Island", "path": BASE_DIR / "assets/map415.png"},
  {"local": "Seafoam Island", "path": BASE_DIR / "assets/map419.png"},
  {"local": "Tarroco Island", "path": BASE_DIR / "assets/map327.png"},
  {
    "local": "Charicific Valley",
    "path": BASE_DIR / "assets/map601.png"
  },
  {
    "local": "Charicific Valley",
    "path": BASE_DIR / "assets/map602.png"
  },
  {
    "local": "Pewter",
    "path": BASE_DIR / "assets/map603.png"
  },
  {
    "local": "Hurricane Island",
    "path": BASE_DIR / "assets/map604.png"
  },
  {
    "local": "Hurricane Island",
    "path": BASE_DIR / "assets/map605.png"
  },
  {
    "local": "Cubone's Lair",
    "path": BASE_DIR / "assets/map606.png"
  },
  {
    "local": "Cerulean",
    "path": BASE_DIR / "assets/map607.png"
  },
  {
    "local": "Lightstorm Island",
    "path": BASE_DIR / "assets/map608.png"
  },
  {
    "local": "Viridian Forest (subsolo)",
    "path": BASE_DIR / "assets/map609.png"
  },
  {
    "local": "Cubone de Saffron",
    "path": BASE_DIR / "assets/map610.png"
  },
  {
    "local": "Saffron e Lavender (subsolo)",
    "path": BASE_DIR / "assets/map611.png"
  },
  {
    "local": "Tangelo Island",
    "path": BASE_DIR / "assets/map612.png"
  },
  {
    "local": "Lakeshore Island",
    "path": BASE_DIR / "assets/map613.png"
  },
  {
    "local": "Fairchild Island (Giant Pidgeot)",
    "path": BASE_DIR / "assets/map614.png"
  },
  {
    "local": "Magma Island",
    "path": BASE_DIR / "assets/map615.png"
  },
  {
    "local": "Fairchild Island (Stantler)",
    "path": BASE_DIR / "assets/map616.png"
  },
  {
    "local": "Magma Island",
    "path": BASE_DIR / "assets/map617.png"
  },
  {
    "local": "Magma Island",
    "path": BASE_DIR / "assets/map618.png"
  },
  {
    "local": "Pewter (subsolo)",
    "path": BASE_DIR / "assets/map619.png"
  },
  {
    "local": "Cinnabar",
    "path": BASE_DIR / "assets/map620.png"
  },
  {
    "local": "Fairchild Island",
    "path": BASE_DIR / "assets/map621.png"
  },
  {
    "local": "Fairchild Island",
    "path": BASE_DIR / "assets/map622.png"
  },
  {
    "local": "Jungle Island",
    "path": BASE_DIR / "assets/map623.png"
  },
  {
    "local": "Mt. Moon (Sandslash)",
    "path": BASE_DIR / "assets/map624.png"
  },
  {
    "local": "Mt. Moon",
    "path": BASE_DIR / "assets/map625.png"
  },
  {
    "local": "Mt. Moon",
    "path": BASE_DIR / "assets/map626.png"
  },
  {
    "local": "Cleopatra Island",
    "path": BASE_DIR / "assets/map627.png"
  },
  {
    "local": "Cleopatra Island",
    "path": BASE_DIR / "assets/map628.png"
  },
  {
    "local": "Cleopatra Island",
    "path": BASE_DIR / "assets/map629.png"
  },
  {
    "local": "Cleopatra Island",
    "path": BASE_DIR / "assets/map630.png"
  },
  {
    "local": "Saffron",
    "path": BASE_DIR / "assets/map631.png"
  },
  {
    "local": "Vermilion",
    "path": BASE_DIR / "assets/map632.png"
  },
  {
    "local": "Saffron",
    "path": BASE_DIR / "assets/map633.png"
  },
  {
    "local": "Cubone's Lair",
    "path": BASE_DIR / "assets/map634.png"
  },
  {
    "local": "Vermilion",
    "path": BASE_DIR / "assets/map635.png"
  },
  {
    "local": "Fuchsia",
    "path": BASE_DIR / "assets/map636.png"
  },
  {
    "local": "Moro Island",
    "path": BASE_DIR / "assets/map637.png"
  },
  {
    "local": "Ascorbia Island",
    "path": BASE_DIR / "assets/map638.png"
  },
  {
    "local": "Lost Island",
    "path": BASE_DIR / "assets/map638.png"
  },

  {
    "local": "Pewter",
    "path": BASE_DIR / "assets/map401.png"
  },
  {
    "local": "Pewter",
    "path": BASE_DIR / "assets/map402.png"
  },
  {
    "local": "Mt. Moon",
    "path": BASE_DIR / "assets/map403.png"
  },
  {
    "local": "Mt. Moon",
    "path": BASE_DIR / "assets/map404.png"
  },
  {
    "local": "Rock Tunnel",
    "path": BASE_DIR / "assets/map405.png"
  },
  {
    "local": "Power Plant (Caminho da Outland South)",
    "path": BASE_DIR / "assets/map406.png"
  },
  {
    "local": "Saffron",
    "path": BASE_DIR / "assets/map407.png"
  },
  {
    "local": "Machop de Lavender",
    "path": BASE_DIR / "assets/map408.png"
  },
  {
    "local": "Rock Tunnel",
    "path": BASE_DIR / "assets/map409.png"
  },
  {
    "local": "Tangelo Island (Golem)",
    "path": BASE_DIR / "assets/map410.png"
  },
  {
    "local": "Tangelo Island (Golduck)",
    "path": BASE_DIR / "assets/map411.png"
  },
  {
    "local": "Trovitopolis City (Snorlax)",
    "path": BASE_DIR / "assets/map412.png"
  },
  {
    "local": "Cinnabar",
    "path": BASE_DIR / "assets/map413.png"
  },
  {
    "local": "Cinnabar",
    "path": BASE_DIR / "assets/map414.png"
  },
  {
    "local": "Fairchild Island",
    "path": BASE_DIR / "assets/map415.png"
  },
  {
    "local": "Fairchild Island (Steelix)",
    "path": BASE_DIR / "assets/map416.png"
  },
  {
    "local": "Fairchild Island (Giant Rhydon)",
    "path": BASE_DIR / "assets/map417.png"
  },
  {
    "local": "Fire Island",
    "path": BASE_DIR / "assets/map418.png"
  },
  {
    "local": "Seafoam Island",
    "path": BASE_DIR / "assets/map419.png"
  },
  {
    "local": "Ascorbia Island",
    "path": BASE_DIR / "assets/map420.png"
  },
  {
    "local": "Desert Island",
    "path": BASE_DIR / "assets/map421.png"
  },
  {
    "local": "Pewter",
    "path": BASE_DIR / "assets/map501.png"
  },
  {
    "local": "Pewter",
    "path": BASE_DIR / "assets/map502.png"
  },
  {
    "local": "Shell Island",
    "path": BASE_DIR / "assets/map503.png"
  },
  {
    "local": "Shell Island",
    "path": BASE_DIR / "assets/map504.png"
  },
  {
    "local": "Pewter (Omastar)",
    "path": BASE_DIR / "assets/map505.png"
  },
  {
    "local": "Cerulean",
    "path": BASE_DIR / "assets/map506.png"
  },
  {
    "local": "Cerulean",
    "path": BASE_DIR / "assets/map507.png"
  },
{
    "local": "Ice Island",
    "path": BASE_DIR / "assets/map201.png"
  },
  {
    "local": "Ice Island",
    "path": BASE_DIR / "assets/map202.png"
  },
  {
    "local": "Seafoam Island (left)",
    "path": BASE_DIR / "assets/map203.png"
  },
  {
    "local": "Seafoam Island",
    "path": BASE_DIR / "assets/map204.png"
  },
  {
    "local": "Seafoam Island",
    "path": BASE_DIR / "assets/map205.png"
  },
  {
    "local": "Seafoam Island",
    "path": BASE_DIR / "assets/map206.png"
  },
  {
    "local": "Camping Site",
    "path": BASE_DIR / "assets/map207.png"
  },
  {
    "local": "Seafoam Island",
    "path": BASE_DIR / "assets/map208.png"
  }
]
