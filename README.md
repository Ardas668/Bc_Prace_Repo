# Bc_Prace_Repo

Navod na spusteni skriptu

1) Pres powershell/bash spustit platformu Ollama skrz prikaz "Ollama serve"
2) Spustit Neo4J desktop a spustit lokalni instanci
3) Ve skriptu lze upravit nasledujici promenne:
   session a auth zde zadat jmeno a heslo lokalni instance v neo4j, ktera se nastavuje pri jejim zalozeni
   zdroj = kde je umisten .txt soubor ze ktereho se ma cist. r na zactku je dulezite kvuli lomitkum
   uvnitr nastaveni llm Ollama lze zmenit model, ktery meni jaky nainstalovany model se pouziva, temperature, ktera urcuje jak moc si model "vymysli" a base_url je lokalni adresa Ollamy
   Dale nic neupravovat.
4)Po skonceni skriptu (dokud neni napsano hotovo, muze trvat od minuty po hodiny v zavislosti na vypocetni sile pocitace a zvoleneho modelu) otevrit neo4j desktop, sekce query, vpravo nahore napsat "MATCH (n)-[r]->(m) RETURN n,r,m. Vyhodi to, ze nejste pripojeni k instanci tak jen zvolite tu lokalni
5) Hotovo, muzete si s tím hrat

