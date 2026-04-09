from langchain_ollama import ChatOllama
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_core.documents import Document
from neo4j import GraphDatabase
import re

zdroj = r"C:\Users\theod\Desktop\pokus.txt" ## to "r" na zacatku musi byt kvuli lomitkum
session = "neo4j"
auth = "12345678"

llm = ChatOllama( ## Nastaveni spojeni s lokalnim modelem. Lze pouzit jiny model, staci prepsat hodnotu promenne model.
    model="qwen3:14b",
    temperature=0, 
    base_url="http://127.0.0.1:11434"
)
## Odsud dal uz nic nemenit

extraktor = LLMGraphTransformer(llm=llm) ## Nastaveni extraktoru entit a vzytahu

with open(zdroj, "r", encoding="utf-8") as file: ## otevreni .txt souboru. 
    TEXT = file.read()
    
vysledky = extraktor.convert_to_graph_documents([Document(page_content=TEXT)]) ## dodani textu extraktoru

driver = GraphDatabase.driver("bolt://localhost:7687", auth=(session, auth)) ## Zadefinovani propojeni s neo4j. Jmeno local session a heslo pro ni.
with driver.session() as session:
    session.run("MATCH (n) DETACH DELETE n") ## Smazani predchoziho grafu 
    for doc in vysledky:
        for uzel in doc.nodes: ## Kazdemu nalezenemu uzlu, ktery model nasel, se vytvori v neo4j uzel
            session.run(
                "MERGE (n:Entita {id: $id}) SET n.jmeno = $id, n.typ = $typ",
                id=uzel.id, typ=uzel.type
            )
        for vztah in doc.relationships:
            
            typ = vztah.type.upper() ##Cypher netoleruje mezery, diakritiku a jine nez alfanumericke znaky v nazvu vztahu. Proto se nejdriv odstrani diakritika a potom regexem vse co nejsou pismena ci cisla
            typ = typ.replace('Á','A').replace('É','E').replace("Í","I").replace("Ó","O").replace("Ú","U").replace("Ý","Y").replace("Č","C").replace("Ď","D").replace("Ě","E").replace("Ň","N").replace("Ř","R").replace("Š","S").replace("Ť","T").replace("Ž","Z").replace('Ů','U')
            typ = re.sub(r'[^A-Z0-9_]', '_', typ)
            session.run(f""" 
                MATCH (a:Entita {{id: $zdroj}}), (b:Entita {{id: $cil}})  
                MERGE (a)-[r:{typ}]->(b)
            """, zdroj=vztah.source.id, cil=vztah.target.id) ## Dodani propojeni vztahu mezi uzly

print("MATCH (n)-[r]->(m) RETURN n,r,m") ## Pripominka co napsat do query v Neo4J desktop
driver.close()

print("Hotovo")
