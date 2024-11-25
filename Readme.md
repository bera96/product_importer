# Product Importer API

A FastAPI-based REST API service that imports product data in XML format into a MongoDB database.

## Features
- Product data import via XML file or XML content
- Asynchronous XML parsing
- MongoDB integration
- Docker support
- Test coverage monitoring

## Requirements
- Docker
- Docker Compose

## Kurulum

1. Clone the project:

    ```bash
    git clone <repo-url>
    cd product_importer
    ```

2. Run with docker:

     ```bash
    docker-compose up --build
    ````

## Sample XML

```xml
<?xml version="1.0"?>
<Products>
  <Product ProductId="27356-01" Name="NAKIŞLI ELBİSE">
   <Images>
        <Image Path="www.aday-butik-resim-sitesi/27356-turuncu-1.jpeg"></Image>
        <Image Path="www.aday-butik-resim-sitesi/27356-turuncu-2.jpeg"></Image>
        <Image Path="www.aday-butik-resim-sitesi/27356-turuncu-3.jpeg"></Image>
    </Images>
    <ProductDetails>
    <ProductDetail Name="Price" Value="5,24"/>
    <ProductDetail Name="DiscountedPrice" Value="2,24"/>
    <ProductDetail Name="ProductType" Value="Elbise"/>
    <ProductDetail Name="Quantity" Value="9"/>
    <ProductDetail Name="Color" Value="Turuncu"/>
    <ProductDetail Name="Series" Value="1S-1M-2L-1XL"/>
    <ProductDetail Name="Season" Value="2023 Kış"/>
    </ProductDetails>
    <Description>
<![CDATA[<ul><li><strong>Ürün Bilgisi:</strong>Kruvaze yaka, uzun kollu, düşük omuzlu, astarlı, crop boy, tam kalıp, düz kesim, blazer ceket</li><li><strong>Kumaş Bilgisi:</strong>%90 Polyester %10 Likra</li><li><strong>Ürün Ölçüleri1:</strong>&nbsp;Boy: 42 cm Kol: 62 cm</li><li><strong>Model Ölçüleri:</strong>&nbsp;Boy: 1.72, Göğüs: 86,&nbsp;Bel: 64, Kalça: 90</li><li>Modelin üzerindeki ürün <strong>S/36</strong>&nbsp;bedendir.</li><li>Bedenler arası +/- sapma olabilir.</li></ul>]]>
</Description>
  </Product>
  <Product ProductId="27356-02" Name="NAKIŞLI ELBİSE">
   <Images>
        <Image Path="www.aday-butik-resim-sitesi/27356-sarı-1.jpeg"></Image>
        <Image Path="www.aday-butik-resim-sitesi/27356-sarı-2.jpeg"></Image>
        <Image Path="www.aday-butik-resim-sitesi/27356-sarı-3.jpeg"></Image>
    </Images>
    <ProductDetails>
    <ProductDetail Name="Price" Value="5,24"/>
    <ProductDetail Name="DiscountedPrice" Value="5,24"/>
    <ProductDetail Name="ProductType" Value="Elbise"/>
    <ProductDetail Name="Quantity" Value="0"/>
    <ProductDetail Name="Color" Value="Sarı"/>
    <ProductDetail Name="Series" Value="1S-1M-1L-1XL"/>
    <ProductDetail Name="Season" Value="2023 Kış"/>
    </ProductDetails>
    <Description>
<![CDATA[<ul><li><strong>Ürün Bilgisi: </strong>v yaka, kısa kollu, pamuklu, terletmez, iç göstermez, parlak kumaş, standart boy, düz kesim, tan kalıp, gri tişört</li><li><strong>Kumaş Bilgisi:</strong> %100 Pamuklu</li><li><strong>Ürün Ölçüleri:</strong> Boy: 62 cm</li><li><strong>Model Ölçüleri:</strong> Boy: 1.74, Göğüs: 85, Bel: 64, Kalça: 91</li><li>Modelin üzerindeki ürün <strong>S/36</strong> bedendir.</li><li>Bedenler arası +/- 2cm fark olmaktadır.</li></ul>]]>
</Description>
  </Product>

   <Product ProductId="62156-01" Name="Büzgü Kollu T-shirt">
   <Images>
        <Image Path="www.aday-butik-resim-sitesi/62156-ekru-1.jpeg"></Image>
        <Image Path="www.aday-butik-resim-sitesi/62156-ekru-2.jpeg"></Image>
        <Image Path="www.aday-butik-resim-sitesi/62156-ekru-3.jpeg"></Image>
    </Images>
    <ProductDetails>
    <ProductDetail Name="Price" Value="3,24"/>
    <ProductDetail Name="DiscountedPrice" Value="0"/>
    <ProductDetail Name="ProductType" Value="T-shirt"/>
    <ProductDetail Name="Quantity" Value="0"/>
    <ProductDetail Name="Color" Value="Ekru"/>
    <ProductDetail Name="Series" Value="1M-1L-1XL"/>
    <ProductDetail Name="Season" Value="2023 Yaz"/>
    </ProductDetails>
    <Description>
<![CDATA[<ul><li><strong>Ürün Bilgisi: </strong>Yuvarlak yaka, ince askılı, yanı büzgülü, bağcık detaylı, terletmez, likralı kumaş, dar kalıp, dar kesim, crop</li><li><strong>Kumaş Bilgisi:</strong></li><li><strong>Model Ölçüleri:</strong> Boy: 1.73, Kilo: 50, Göğüs: 87, Bel: 63, Kalça: 88</li></ul>]]>
</Description>
  </Product>

   <Product ProductId="62156-02" Name="Büzgü Kollu T-shirt">
   <Images>
        <Image Path="www.aday-butik-resim-sitesi/62156-vizon-1.jpeg"></Image>
        <Image Path="www.aday-butik-resim-sitesi/62156-vizon-2.jpeg"></Image>
        <Image Path="www.aday-butik-resim-sitesi/62156-vizon-3.jpeg"></Image>
    </Images>
    <Description>
<![CDATA[<ul><li><strong>Ürün Bilgisi: </strong>Polo yaka, düğmeli, göğüs ve sırt dekolteli, likralı, triko kumaş, likralı, crop boy, dar kalıp, dar kesim, bluz</li><li><strong>Kumaş Bilgisi:</strong> Triko</li><li><strong>Model Ölçüleri:</strong> Boy: 1.73, Kilo: 50, Göğüs: 87, Bel: 63, Kalça: 88</li><li>Modelin üzerindeki ürün <strong>STD</strong> bedendir.</li></ul>]]>
</Description>
    <ProductDetails>
    <ProductDetail Name="Price" Value="3,24"/>
    <ProductDetail Name="DiscountedPrice" Value="1,24"/>
    <ProductDetail Name="ProductType" Value="T-shirt"/>
    <ProductDetail Name="Quantity" Value="0"/>
    <ProductDetail Name="Color" Value="Vizon"/>
    <ProductDetail Name="Series" Value="1M-1L-1XL"/>
    <ProductDetail Name="Season" Value="2023 Yaz"/>
    </ProductDetails>
  </Product>
</Products>
```


## API Endpoints

### POST /api/v1/import-products

Imports product data from an XML file or XML content.

**Usage:**

1. Upload an XML file using form-data:

    ```bash
    curl -X POST http://localhost:8000/api/v1/import-products \
    -F "file=@....your-path/sample.xml"
    ```

2. Send XML content in the request body:

    ```bash
    curl -X POST http://localhost:8000/api/v1/import-products \
    -H "Content-Type: application/xml" \
    -d @sample.xml
    ```
    Alternatively, you can use tools like Postman.

## Logs

Application logs are stored daily in the logs/ directory:
- General logs: `app_YYYYMMDD.log`

    