# Исследование информации о состоянии беспроводных сетей


## Цель работы

1.  Получить знания о методах исследования радиоэлектронной обстановки.
2.  Составить представление о механизмах работы Wi-Fi сетей на канальном
    и сетевом уровне модели OSI.
3.  Зекрепить практические навыки использования языка программирования R
    для обработки данных
4.  Закрепить знания основных функций обработки данных экосистемы
    tidyverse языка R

## Исходные данные

1.  Rstudio Desktop
2.  Наше рабочее окружение

## План

1.  Импортировать данные.
2.  Привести датасеты в вид “аккуратных данных”, преобразовать типы
    столбцов в соответствии с типом данных
3.  Просмотреть общую структуру данных с помощью функции glimpse()

## Шаги:

``` r
sessionInfo()
```

    R version 4.5.1 (2025-06-13 ucrt)
    Platform: x86_64-w64-mingw32/x64
    Running under: Windows 11 x64 (build 26100)

    Matrix products: default
      LAPACK version 3.12.1

    locale:
    [1] LC_COLLATE=Russian_Russia.utf8  LC_CTYPE=Russian_Russia.utf8   
    [3] LC_MONETARY=Russian_Russia.utf8 LC_NUMERIC=C                   
    [5] LC_TIME=Russian_Russia.utf8    

    time zone: Europe/Moscow
    tzcode source: internal

    attached base packages:
    [1] stats     graphics  grDevices utils     datasets  methods   base     

    loaded via a namespace (and not attached):
     [1] compiler_4.5.1    fastmap_1.2.0     cli_3.6.5         tools_4.5.1      
     [5] htmltools_0.5.8.1 rstudioapi_0.17.1 yaml_2.3.10       rmarkdown_2.30   
     [9] knitr_1.50        jsonlite_2.0.0    xfun_0.53         digest_0.6.37    
    [13] rlang_1.1.6       evaluate_1.0.5   

## Подготовка данных

1\. Импортировали данные.

``` r
library(tidyverse)
```

    Warning: пакет 'tidyverse' был собран под R версии 4.5.2

    Warning: пакет 'ggplot2' был собран под R версии 4.5.2

    Warning: пакет 'tidyr' был собран под R версии 4.5.2

    Warning: пакет 'readr' был собран под R версии 4.5.2

    Warning: пакет 'purrr' был собран под R версии 4.5.2

    Warning: пакет 'dplyr' был собран под R версии 4.5.2

    Warning: пакет 'forcats' был собран под R версии 4.5.2

    Warning: пакет 'lubridate' был собран под R версии 4.5.2

    ── Attaching core tidyverse packages ──────────────────────── tidyverse 2.0.0 ──
    ✔ dplyr     1.1.4     ✔ readr     2.1.6
    ✔ forcats   1.0.1     ✔ stringr   1.5.2
    ✔ ggplot2   4.0.1     ✔ tibble    3.3.0
    ✔ lubridate 1.9.4     ✔ tidyr     1.3.1
    ✔ purrr     1.2.0     
    ── Conflicts ────────────────────────────────────────── tidyverse_conflicts() ──
    ✖ dplyr::filter() masks stats::filter()
    ✖ dplyr::lag()    masks stats::lag()
    ℹ Use the conflicted package (<http://conflicted.r-lib.org/>) to force all conflicts to become errors

``` r
url <- "https://storage.yandexcloud.net/dataset.ctfsec/P2_wifi_data.csv"
```

2\. Привели датасеты в вид “аккуратных данных”, преобразовали типы
столбцов в соответствии с типом данных

``` r
raw_text <- read_file(url)
lines <- str_split(raw_text, "\n", simplify = TRUE)[1,]
client_line <- which(str_detect(lines, "Station MAC"))
if (length(client_line) > 0) {
  ap_text <- lines[1:(client_line - 2)]
  client_text <- lines[client_line:length(lines)]
  ap_raw <- read_csv(I(ap_text))
  client_raw <- read_csv(I(client_text))
}
```

    Rows: 167 Columns: 15
    ── Column specification ────────────────────────────────────────────────────────
    Delimiter: ","
    chr  (6): BSSID, Privacy, Cipher, Authentication, LAN IP, ESSID
    dbl  (6): channel, Speed, Power, # beacons, # IV, ID-length
    lgl  (1): Key
    dttm (2): First time seen, Last time seen

    ℹ Use `spec()` to retrieve the full column specification for this data.
    ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

    Warning: One or more parsing issues, call `problems()` on your data frame for details,
    e.g.:
      dat <- vroom(...)
      problems(dat)

    Rows: 12081 Columns: 7
    ── Column specification ────────────────────────────────────────────────────────
    Delimiter: ","
    chr  (3): Station MAC, BSSID, Probed ESSIDs
    dbl  (2): Power, # packets
    dttm (2): First time seen, Last time seen

    ℹ Use `spec()` to retrieve the full column specification for this data.
    ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

``` r
ap_tidy <- ap_raw %>%
  rename(
    beacons = `# beacons`,
    IV = `# IV`
  ) %>%
  mutate(
    `First time seen` = ymd_hms(`First time seen`),
    `Last time seen` = ymd_hms(`Last time seen`),
    channel = as.integer(channel),
    Speed = as.numeric(Speed),
    Power = as.integer(Power),
    beacons = as.integer(beacons),
    IV = as.integer(IV),
    `ID-length` = as.integer(`ID-length`)
  )
```

``` r
client_tidy <- client_raw %>%
  rename(
    packets = `# packets`
  ) %>%
  mutate(
    `First time seen` = ymd_hms(`First time seen`),
    `Last time seen` = ymd_hms(`Last time seen`),
    Power = as.integer(Power),
    packets = as.integer(packets)
  )
```

3\. Просмотрели общую структуру данных с помощью функции glimpse()

``` r
glimpse(ap_tidy)
```

    Rows: 167
    Columns: 15
    $ BSSID             <chr> "BE:F1:71:D5:17:8B", "6E:C7:EC:16:DA:1A", "9A:75:A8:…
    $ `First time seen` <dttm> 2023-07-28 09:13:03, 2023-07-28 09:13:03, 2023-07-2…
    $ `Last time seen`  <dttm> 2023-07-28 11:50:50, 2023-07-28 11:55:12, 2023-07-2…
    $ channel           <int> 1, 1, 1, 7, 6, 6, 11, 11, 11, 1, 6, 14, 11, 11, 6, 6…
    $ Speed             <dbl> 195, 130, 360, 360, 130, 130, 195, 130, 130, 195, 18…
    $ Privacy           <chr> "WPA2", "WPA2", "WPA2", "WPA2", "WPA2", "OPN", "WPA2…
    $ Cipher            <chr> "CCMP", "CCMP", "CCMP", "CCMP", "CCMP", NA, "CCMP", …
    $ Authentication    <chr> "PSK", "PSK", "PSK", "PSK", "PSK", NA, "PSK", "PSK",…
    $ Power             <int> -30, -30, -68, -37, -57, -63, -27, -38, -38, -66, -4…
    $ beacons           <int> 846, 750, 694, 510, 647, 251, 1647, 1251, 704, 617, …
    $ IV                <int> 504, 116, 26, 21, 6, 3430, 80, 11, 0, 0, 86, 0, 0, 0…
    $ `LAN IP`          <chr> "0.  0.  0.  0", "0.  0.  0.  0", "0.  0.  0.  0", "…
    $ `ID-length`       <int> 12, 4, 2, 14, 25, 13, 12, 13, 24, 12, 10, 0, 24, 24,…
    $ ESSID             <chr> "C322U13 3965", "Cnet", "KC", "POCO X5 Pro 5G", NA, …
    $ Key               <lgl> NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, …

``` r
glimpse(client_tidy)
```

    Rows: 12,081
    Columns: 7
    $ `Station MAC`     <chr> "CA:66:3B:8F:56:DD", "96:35:2D:3D:85:E6", "5C:3A:45:…
    $ `First time seen` <dttm> 2023-07-28 09:13:03, 2023-07-28 09:13:03, 2023-07-2…
    $ `Last time seen`  <dttm> 2023-07-28 10:59:44, 2023-07-28 09:13:03, 2023-07-2…
    $ Power             <int> -33, -65, -39, -61, -53, -43, -31, -71, -74, -65, -4…
    $ packets           <int> 858, 4, 432, 958, 1, 344, 163, 3, 115, 437, 265, 77,…
    $ BSSID             <chr> "BE:F1:71:D5:17:8B", "(not associated)", "BE:F1:71:D…
    $ `Probed ESSIDs`   <chr> "C322U13 3965", "IT2 Wireless", "C322U21 0566", "C32…

## Анализ

### Точки доступа

1\. Определили небезопасные точки доступа (без шифрования – OPN)

``` r
ap_tidy %>%
  filter(Privacy == "OPN") %>%
  count()
```

    # A tibble: 1 × 1
          n
      <int>
    1    42

2\. Определили производителя для каждого обнаруженного устройства

``` r
ap_tidy <- ap_tidy %>%
  mutate(
    OUI = substr(gsub(":", "", BSSID), 1, 6)
  )
ap_tidy %>% select(BSSID, OUI, ESSID) %>% head(10)
```

    # A tibble: 10 × 3
       BSSID             OUI    ESSID                   
       <chr>             <chr>  <chr>                   
     1 BE:F1:71:D5:17:8B BEF171 C322U13 3965            
     2 6E:C7:EC:16:DA:1A 6EC7EC Cnet                    
     3 9A:75:A8:B9:04:1E 9A75A8 KC                      
     4 4A:EC:1E:DB:BF:95 4AEC1E POCO X5 Pro 5G          
     5 D2:6D:52:61:51:5D D26D52 <NA>                    
     6 E8:28:C1:DC:B2:52 E828C1 MIREA_HOTSPOT           
     7 BE:F1:71:D6:10:D7 BEF171 C322U21 0566            
     8 0A:C5:E1:DB:17:7B 0AC5E1 AndroidAP177B           
     9 38:1A:52:0D:84:D7 381A52 EBFCD57F-EE81fI_DL_1AO2T
    10 BE:F1:71:D5:0E:53 BEF171 C322U06 9080            

3\. Выявили устройства, использующие последнюю версию протокола
шифрования WPA3, и названия точек доступа, реализованных на этих
устройствах

``` r
ap_tidy %>%
    filter(Authentication == "SAE PSK" | Privacy == "WPA3 WPA2") %>%
    distinct(ESSID) %>%
    arrange(ESSID)  %>% print()
```

    # A tibble: 5 × 1
      ESSID                                         
      <chr>                                         
    1 "Christie’s"                                  
    2 "iPhone (Анастасия)"                          
    3 "iPhone XS Max \U0001f98a\U0001f431\U0001f98a"
    4 "Димасик"                                     
    5  <NA>                                         

4\. Отсортировали точки доступа по интервалу времени, в течение которого
они находились на связи, по убыванию.

``` r
ap_tidy <- ap_tidy %>%
  mutate(Connection_duration = as.numeric(difftime(`Last time seen`, 
                                                   `First time seen`, 
                                                   units = "mins")))
ap_sorted_by_time <- ap_tidy %>% arrange(desc(Connection_duration))
ap_tidy %>% arrange(desc(Connection_duration)) %>% print()
```

    # A tibble: 167 × 17
       BSSID    `First time seen`   `Last time seen`    channel Speed Privacy Cipher
       <chr>    <dttm>              <dttm>                <int> <dbl> <chr>   <chr> 
     1 00:25:0… 2023-07-28 09:13:06 2023-07-28 11:56:21      44    -1 OPN     <NA>  
     2 E8:28:C… 2023-07-28 09:13:09 2023-07-28 11:56:05      11   130 OPN     <NA>  
     3 E8:28:C… 2023-07-28 09:13:03 2023-07-28 11:55:38       6   130 OPN     <NA>  
     4 08:3A:2… 2023-07-28 09:13:27 2023-07-28 11:55:53      14    -1 WPA     <NA>  
     5 6E:C7:E… 2023-07-28 09:13:03 2023-07-28 11:55:12       1   130 WPA2    CCMP  
     6 E8:28:C… 2023-07-28 09:13:06 2023-07-28 11:55:12       6   130 OPN     <NA>  
     7 E8:28:C… 2023-07-28 09:13:06 2023-07-28 11:55:11       6   130 OPN     <NA>  
     8 48:5B:3… 2023-07-28 09:13:06 2023-07-28 11:55:11       1   270 WPA2    CCMP  
     9 E8:28:C… 2023-07-28 09:13:06 2023-07-28 11:55:10       6    -1 OPN     <NA>  
    10 8E:55:4… 2023-07-28 09:13:06 2023-07-28 11:55:09       6    65 WPA2    CCMP  
    # ℹ 157 more rows
    # ℹ 10 more variables: Authentication <chr>, Power <int>, beacons <int>,
    #   IV <int>, `LAN IP` <chr>, `ID-length` <int>, ESSID <chr>, Key <lgl>,
    #   OUI <chr>, Connection_duration <dbl>

5\. Обнаружили топ-10 самых быстрых точек доступа.

``` r
ap_tidy %>%
      arrange(desc(Speed)) %>%
      select(BSSID, ESSID, Speed) %>%
      head(10)
```

    # A tibble: 10 × 3
       BSSID             ESSID              Speed
       <chr>             <chr>              <dbl>
     1 26:20:53:0C:98:E8 <NA>                 866
     2 96:FF:FC:91:EF:64 <NA>                 866
     3 CE:48:E7:86:4E:33 iPhone (Анастасия)   866
     4 8E:1F:94:96:DA:FD iPhone (Анастасия)   866
     5 9A:75:A8:B9:04:1E KC                   360
     6 4A:EC:1E:DB:BF:95 POCO X5 Pro 5G       360
     7 56:C5:2B:9F:84:90 OnePlus 6T           360
     8 E8:28:C1:DC:B2:41 MIREA_GUESTS         360
     9 E8:28:C1:DC:B2:40 MIREA_HOTSPOT        360
    10 E8:28:C1:DC:B2:42 <NA>                 360

6\. Отсортировали точки доступа по частоте отправки запросов (beacons) в
единицу времени по их убыванию

``` r
ap_tidy %>%
      mutate(Beacon_rate = beacons / Connection_duration) %>%
      arrange(desc(Beacon_rate)) %>%
      select(BSSID, ESSID, beacons, Connection_duration, Beacon_rate)
```

    # A tibble: 167 × 5
       BSSID             ESSID               beacons Connection_duration Beacon_rate
       <chr>             <chr>                 <int>               <dbl>       <dbl>
     1 76:E4:ED:B0:5C:9A Инет от Путина            1                   0         Inf
     2 C2:B5:D7:7F:07:A8 DIRECT-a8-HP M227f…       1                   0         Inf
     3 E8:28:C1:DE:47:D1 <NA>                      1                   0         Inf
     4 A2:FE:FF:B8:9B:C9 Christie’s                1                   0         Inf
     5 BA:2A:7A:DD:38:3E Айфон (Oleg)              1                   0         Inf
     6 76:5E:F3:F9:A5:1C Redmi 9C NFC              1                   0         Inf
     7 00:03:7F:12:34:56 MT_FREE                   1                   0         Inf
     8 E0:D9:E3:49:00:B1 <NA>                      1                   0         Inf
     9 E8:28:C1:DC:BD:52 MIREA_HOTSPOT             1                   0         Inf
    10 00:26:CB:AA:62:72 GIVC                      1                   0         Inf
    # ℹ 157 more rows

### Данные клиентов

1\. Определить производителя для каждого обнаруженного устройства

``` r
top_ouis <- client_tidy %>%
  mutate(OUI = substr(gsub(":", "", `Station MAC`), 1, 6)) %>%
  count(OUI, sort = TRUE) %>%
  head(20)

top_ouis
```

    # A tibble: 20 × 2
       OUI        n
       <chr>  <int>
     1 BCF171    52
     2 0EEF92    36
     3 DAA119    33
     4 FE41FA    32
     5 105107    25
     6 5AABCF    18
     7 A402B9    17
     8 E2CCF8    10
     9 8C554A     7
    10 12BBF3     5
    11 503EAA     5
    12 701AB8     5
    13 381A52     4
    14 009569     3
    15 1CBFC0     3
    16 3C135A     3
    17 922064     3
    18 961700     3
    19 00E93A     2
    20 02F711     2

``` r
client_oui_db_large <- tribble(
  ~OUI, ~Manufacturer,
  "CA663B", "Apple",
  "96352D", "Huawei",
  "A4F1E8", "Apple",
  "C4E984", "TP-Link",
  "E828C1", "Apple",
  "D26D52", "Huawei",
  "5C3A45", "Samsung",
  "C0E434", "AzureWave",
  "68545A", "Samsung",
  "CA54C4", "Huawei",
  "4AC928", "Huawei",
  "A0E70B", "Intel",
  "009569", "NVIDIA",
  "00E93A", "HTC",
  "00F48D", "Huawei",
  "04C06F", "TP-Link",
  "080028", "Apple",
  "0C8BFD", "Intel",
  "10C07C", "Broadcom"
)
```

Объединяем с нашими данными

``` r
client_tidy <- client_tidy %>%
  mutate(OUI = substr(gsub(":", "", `Station MAC`), 1, 6)) %>%
  left_join(client_oui_db_large, by = "OUI")
```

Проверяе что устройства получили производителя

``` r
client_tidy %>%
  select(`Station MAC`, Manufacturer) %>%
  head(20)
```

    # A tibble: 20 × 2
       `Station MAC`     Manufacturer
       <chr>             <chr>       
     1 CA:66:3B:8F:56:DD Apple       
     2 96:35:2D:3D:85:E6 Huawei      
     3 5C:3A:45:9E:1A:7B Samsung     
     4 C0:E4:34:D8:E7:E5 AzureWave   
     5 5E:8E:A6:5E:34:81 <NA>        
     6 10:51:07:CB:33:E7 <NA>        
     7 68:54:5A:40:35:9E Samsung     
     8 74:4C:A1:70:CE:F7 <NA>        
     9 8A:A3:5A:33:76:57 <NA>        
    10 CA:54:C4:8B:B5:3A Huawei      
    11 BC:F1:71:D4:DB:04 <NA>        
    12 4A:C9:28:46:EE:3F Huawei      
    13 A6:EC:3C:AB:BA:10 <NA>        
    14 4C:44:5B:14:76:E3 <NA>        
    15 9E:01:46:3E:EF:4E <NA>        
    16 A0:E7:0B:AE:D5:44 Intel       
    17 00:95:69:E7:7F:35 NVIDIA      
    18 00:95:69:E7:7C:ED NVIDIA      
    19 14:13:33:59:9F:AB <NA>        
    20 10:51:07:FE:77:BB <NA>        

2\. Обнаружить устройства, которые НЕ рандомизируют свой MAC адрес

``` r
client_tidy %>%
  group_by(`Station MAC`) %>%
  summarise(
    Different_networks = n_distinct(`Probed ESSIDs`, na.rm = TRUE),
    Total_probes = n(),
    .groups = "drop") %>%
  filter(Different_networks > 1) %>%
  arrange(desc(Different_networks))
```

    # A tibble: 0 × 3
    # ℹ 3 variables: Station MAC <chr>, Different_networks <int>,
    #   Total_probes <int>

3\. Кластеризовать запросы от устройств к точкам доступа по их именам.
Определить время появления устройства в зоне радиовидимости и время
выхода его из нее.

``` r
client_tidy %>%
  filter(!is.na(`Probed ESSIDs`) & `Probed ESSIDs` != "") %>%
  group_by(`Station MAC`, `Probed ESSIDs`) %>%
  summarise(
    First_seen = min(`First time seen`),
    Last_seen = max(`Last time seen`),
    Duration_minutes = as.numeric(difftime(max(`Last time seen`), 
                                          min(`First time seen`), 
                                          units = "mins")),
    Avg_power = mean(Power, na.rm = TRUE),
    .groups = "drop"
  )%>%
  arrange(desc(Duration_minutes)) %>%
  head(10)
```

    # A tibble: 10 × 6
       `Station MAC`     `Probed ESSIDs`     First_seen          Last_seen          
       <chr>             <chr>               <dttm>              <dttm>             
     1 00:95:69:E7:7C:ED nvripcsuite         2023-07-28 09:13:11 2023-07-28 11:56:13
     2 00:95:69:E7:7D:21 nvripcsuite         2023-07-28 09:13:15 2023-07-28 11:56:17
     3 8C:55:4A:DE:F2:38 MIREA_HOTSPOT,Gala… 2023-07-28 09:13:17 2023-07-28 11:56:16
     4 00:95:69:E7:7F:35 nvripcsuite         2023-07-28 09:13:11 2023-07-28 11:56:07
     5 70:66:55:D0:B6:C7 MIREA_HOTSPOT       2023-07-28 09:14:09 2023-07-28 11:56:21
     6 CA:54:C4:8B:B5:3A GIVC                2023-07-28 09:13:06 2023-07-28 11:55:04
     7 F6:4D:98:98:18:C3 GIVC                2023-07-28 09:14:37 2023-07-28 11:55:29
     8 C0:E4:34:D8:E7:E5 C322U13 3965        2023-07-28 09:13:03 2023-07-28 11:53:16
     9 5C:3A:45:9E:1A:7B C322U21 0566        2023-07-28 09:13:03 2023-07-28 11:51:54
    10 28:7F:CF:23:25:53 KC                  2023-07-28 09:13:14 2023-07-28 11:51:50
    # ℹ 2 more variables: Duration_minutes <dbl>, Avg_power <dbl>

4\. Оценить стабильность уровня сигнала внури кластера во времени.
Выявить наиболее стабильный кластер.

``` r
stability <- client_tidy %>%
  filter(!is.na(`Probed ESSIDs`) & `Probed ESSIDs` != "") %>%
  group_by(`Station MAC`, `Probed ESSIDs`) %>%
  summarise(
    Mean_power = mean(Power, na.rm = TRUE),
    SD_power = sd(Power, na.rm = TRUE),
    Observations = n(),
    .groups = "drop"
  ) %>%
  mutate(
    Stability_index = SD_power / abs(Mean_power),  
    CV_power = (SD_power / abs(Mean_power)) * 100  
  ) %>%
  filter(!is.na(Stability_index) & is.finite(Stability_index))
stability %>%
  arrange(Stability_index) %>%
  head(1)
```

    # A tibble: 0 × 7
    # ℹ 7 variables: Station MAC <chr>, Probed ESSIDs <chr>, Mean_power <dbl>,
    #   SD_power <dbl>, Observations <int>, Stability_index <dbl>, CV_power <dbl>
