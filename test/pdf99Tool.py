# All tools version
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
)
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings,ChatPromptTemplate
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.query_pipeline import QueryPipeline
from llama_index.core.response_synthesizers import TreeSummarize
from llm import llm
from llama_index.core.tools import FunctionTool
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.agent import ReActAgent

chapter_names = """Animaux vivants
Viandes et abats comestibles
Poissons et crustacés, mollusques et autres invertébrés aquatiques
Laits et produits de la laiterie, oeufs d'oiseaux; miel naturel; produits comestibles d'origine animale, non dénommés ni compris ailleurs
Autres produits d'origine animale, non dénommés ni compris ailleurs
Plantes vivantes et produits de la floriculture
Légumes, plantes, racines et tubercules alimentaires
Fruits comestibles; écorces d'agrumes ou de melons
Café, thé, maté et épices
Céréales
Produits de la minoterie; malt; amidons et fécules; inuline; gluten de froment
Graines et fruits oléagineux; graines, semences et fruits divers; plantes industrielles ou médicinales; pailles et fourrages
Gommes, résines et autres sucs et extraits végétaux
Matières à tresser et autres produits d'origine végétale, non dénommés ni compris ailleurs
Graisses et huiles animales ou végétales; produits de leur dissociation; graisses alimentaires élaborées; cires d'origine animale ou végétale
Préparation de viandes,de poissons ou de crustacés, de mollusques ou d'autres invertébrés aquatiques
Sucres et sucreries
Cacao et ses préparations
Préparations à base de céréales, de farines, d'amidons, de fécules ou de lait; pâtisseries
Préparations de légumes, de fruits, ou d'autres parties de plantes
Préparations alimentaires diverses
Boissons, liquides alcooliques et vinaigres
Résidus et déchets des industries alimentaires; aliments préparés pour animaux
Tabacs et succédanés de tabac fabriqués
Sel; soufre; terres et pierres; plâtres, chaux et ciments
Minerais; scories et cendres
Combustibles minéraux, huiles minérales et produits de leur distillation; matières bitumineuses; cires minérales
Produits chimiques inorganiques; composés inorganiques ou organiques de métaux précieux, d'éléments radioactifs, de métaux des terres rares ou d'isotopes
Produits chimiques organiques
Produits pharmaceutiques
Engrais
Extraits tannants ou tinctoriaux; tanins et leurs dérivés; pigments et autres matières colorantes; peintures et vernis; mastics; encres.
Huiles essentielles et résinodes; produits de parfumerie ou de toilette préparés et préparations cosmétiques
Savons, agents de surface organiques, préparations pour lessives, préparations lubrifiantes, cires artificielles, cires préparées, produits d'entretien, bougies et articles similaires, pâtes à modeler, cires pour l'art dentaire et compositions l'ar
Matières albuminodes; produits à base d'amidons ou de fécules modifiés; colles; enzymes
Poudres et explosifs; articles de pyrotechnie; allumettes; alliages pyrophoriques; matières inflammables
Produits photographiques ou cinématographiques
Produits divers des industries chimiques
Matières plastiques et ouvrages en ces matières
Caoutchouc et ouvrages en caoutchouc
Peaux (autres que les pelleteries) et cuirs
Ouvrages en cuir; articles de bourrellerie ou de sellerie; articles de voyage; sacs à main et contenants similaires; ouvrages en botaux
Pelleteries et fourrures; pelleteries factices
Bois, charbon de bois et ouvrages en bois
Liège et ouvrages en liège
Ouvrages de sparterie ou de vannerie
Pâte de bois ou d'autres matières fibreuses cellulosiques; déchets et rebuts de papier ou de carton
Papiers et cartons; ouvrages en pâte de cellulose, en papier ou en carton
Produits de l'édition, de la presse ou des autres industries graphiques; textes manuscrits ou dactylographiés et plans
Soie
Laine, poils fins,ou grossiers; fils et tissus de crin
Coton
Autres fibres textiles végétales; fils de papier et tissus de fils de papier
Filaments synthétiques ou artificiels
Fibres synthétiques ou artificielles discontinues
Ouates, feutres et nontissés; fibres spéciaux; ficelles; cordes et cordages; articles de corderies
Tapis et autres revêtements de sol en matières textiles
Tissus spéciaux; surfaces textiles touffetées; dentelles; tapisseries; passementeries; broderies
Tissus imprégnés, enduits, recouverts ou stratifiés; articles techniques en matières textiles
Etoffes de bonneterie
Vêtements et accessoires du vêtement, en bonneterie
Vêtements et accessoires du vêtement, autres qu'en bonneterie
Autres articles textiles confectionnés; assortiments; friperie et chiffons
Chaussures, guêtres et articles analogues, parties de ces articles
Casquettes et autres coiffures, ainsi que leurs parties
Parapluies, ombrelles, parasols, cannes, Cannes-sièges, fouets, cravaches et leurs parties
Plumes et duvet préparés et articles en plumes ou en duvet; fleurs artificiel
Oeuvres d'art, collections et antiquités
Déchets et débris; balais et brosses; écorces de liège et agglomérés de liège; ouvrages en liège
Perles fines ou de culture, pierres gemmes ou similaires, métaux précieux, plaqués ou doublés de métaux précieux, ainsi que la monture des pierres précieuses ou semi-précieuses; bijouterie; monnaies
Pierres, plâtres, ciments, amiante, mica ou analogues; produits céramiques; verre et ouvrages en verre
Fers, fonte, aciers; ouvrages en ces matières
Ouvrages en fonte, fer ou acier
Cuivre et ouvrages en cuivre
Nickel et ouvrages en nickel
Plomb et ouvrages en plomb
Zinc et ouvrages en zinc
Etain et ouvrages en étain
Autres métaux communs; cermets; ouvrages en métaux communs
Outils et outillage, articles de coutellerie et couverts de table, en métaux communs; parties de ces articles, en métaux communs
Ustensiles et récipients pour la table ou la cuisine, en métaux communs; articles d'hygiène ou de toilette, en métaux communs, ci
Ouvrages divers en métaux communs
Réacteurs nucléaires, chaudières, machines, appareils et engins mécaniques; parties de ces machines ou appareils
Machines, appareils et matériels électriques et leurs parties; appareils d'enregistrement ou de reproduction du son, appareils d'enregistrement ou de reproduction des images et du son en télévision, et parties et accessoires de ces appareils
Véhicules et matériel pour voies ferrées ou similaires, et leurs parties; appareils mécaniques (y compris les treuils) pour la traction des véhicules, et leurs parties
Véhicules automobiles, tracteurs, cycles et autres véhicules terrestres; leurs parties et accessoires
Aéronefs et engins spatiaux, et leurs parties
Bateaux et autres engins flottants
Instruments et appareils d'optique, de photographie ou de cinématographie, de mesure, de contrôle ou de précision; instruments et appareils médico-chirurgicaux; horlogerie; instruments de musique; parties et accessoires de ces instruments ou appareils
Horlogerie et leurs parties"""
chapter_names_list = chapter_names.split('\n')

chapter_numbers = [num for num in range(1, 100) if num not in [77, 98, 99]]

def create_tools_for_chapters(chapter_numbers, chapter_names_list):
    tools = []
    for chapter_num, chapter_name in zip(chapter_numbers, chapter_names_list):
        # Load or generate index
        try:
            storage_context = StorageContext.from_defaults(
                persist_dir=f"./storage/Chap{chapter_num}"
            )
            index = load_index_from_storage(storage_context)
        except:
            # Load data
            docs = SimpleDirectoryReader(
                input_files=[f"./ContentPDFs/Chap{chapter_num}.pdf"]
            ).load_data()

            # Set context window and number of output tokens
            Settings.context_window = 4096
            Settings.num_output = 256

            # Define LLM with specified parameters
            llm = OpenAI(
                temperature=0.2,
                model="gpt-4",
                context_window=Settings.context_window,
                num_output=Settings.num_output
            )

            # Build index
            index = VectorStoreIndex.from_documents(docs, transformations=[SentenceSplitter(chunk_size=512, chunk_overlap=20)], llm=llm)

            # Persist index
            index.storage_context.persist(persist_dir=f"./storage/Chap{chapter_num}")

        # Define chat templates
        chat_text_qa_msgs = [
            ChatMessage(
                role=MessageRole.SYSTEM,
                content="Always answer the question, even if the context isn't helpful."
            ),
            ChatMessage(
                role=MessageRole.USER,
                content=(
                    "Context below.\n"
                    "{context_str}\n"
                    "Given documents and context below, "
                    "answer the question: {query_str}\n"
                ),
            ),
        ]

        # Simplify and condense messages for refinement template
        chat_refine_msgs = [
            ChatMessage(
                role=MessageRole.SYSTEM,
                content="Always answer the question, even if the context isn't helpful."
            ),
            ChatMessage(
                role=MessageRole.USER,
                content=(
                    "Refine the original answer with more context below.\n"
                    "{context_msg}\n"
                    "Given new context, refine the original answer: {query_str}. "
                    "If context isn't useful, output the original answer.\n"
                    "Original Answer: {existing_answer}"
                ),
            ),
        ]

        text_qa_template = ChatPromptTemplate(chat_text_qa_msgs)
        refine_template = ChatPromptTemplate(chat_refine_msgs)
        llm = None
        # Query engine setup
        engine = index.as_query_engine(
            text_qa_template=text_qa_template,
            refine_template=refine_template,
            llm=llm,
            similarity_top_k=5,
        )

        # Tool definition
        tool = QueryEngineTool(
            query_engine=engine,
            metadata=ToolMetadata(
                name=f"Chapitre_{chapter_num}",
                description=(
                    f"Moroccan customs's chapter {chapter_num}:{chapter_name}"
                ),
            ),
        )
        
        tools.append(tool)

    return tools

# Create tools for the specified chapters
query_engine_tools = create_tools_for_chapters(chapter_numbers, chapter_names_list)