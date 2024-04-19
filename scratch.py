import asyncio
from pathlib import Path
from biolink.integrations import Mafft, EntrezClient
from biolink.models import Taxonomy

async def main():
    entrez_client = EntrezClient()
    data = await entrez_client.efetch("taxonomy", "996")
    output = Taxonomy.from_entrez_xml(data)
    print(output.division)
    
if __name__ == "__main__":
    asyncio.run(main())