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

1.  Импортировали данные.

> url \<-
> “https://storage.yandexcloud.net/dataset.ctfsec/P2_wifi_data.csv”

1.  Привели датасеты в вид “аккуратных данных”, преобразовали типы
    столбцов в соответствии с типом данных

> ap_tidy \<- ap_raw %\>% + rename( + beacons = `# beacons`, + IV =
> `# IV` + ) %\>% + mutate( + `First time seen` =
> ymd_hms(`First time seen`), + `Last time seen` =
> ymd_hms(`Last time seen`), + channel = as.integer(channel), + Speed =
> as.numeric(Speed), + Power = as.integer(Power), + beacons =
> as.integer(beacons), + IV = as.integer(IV), + `ID-length` =
> as.integer(`ID-length`) + ) client_tidy \<- client_raw %\>% +
> rename( + packets = `# packets` + ) %\>% + mutate( + `First time seen`
> = ymd_hms(`First time seen`), + `Last time seen` =
> ymd_hms(`Last time seen`), + Power = as.integer(Power), + packets =
> as.integer(packets) + )

1.  Просмотрели общую структуру данных с помощью функции glimpse()

> glimpse(ap_tidy) Rows: 167 Columns: 15 $ BSSID <chr>
> “BE:F1:71:D5:17:8B”, “6E:C7:EC:16:DA:1A… $ `First time seen` <dttm>
> 2023-07-28 09:13:03, 2023-07-28 09:13:… $ `Last time seen` <dttm>
> 2023-07-28 11:50:50, 2023-07-28 11:55:… $ channel <int> 1, 1, 1, 7, 6,
> 6, 11, 11, 11, 1, 6, 14,… $ Speed <dbl> 195, 130, 360, 360, 130, 130,
> 195, 130,… $ Privacy <chr>”WPA2”, “WPA2”, “WPA2”, “WPA2”, “WPA2”,… $
> Cipher <chr> “CCMP”, “CCMP”, “CCMP”, “CCMP”, “CCMP”,… $ Authentication
> <chr> “PSK”, “PSK”, “PSK”, “PSK”, “PSK”, NA, … $ Power <int> -30, -30,
> -68, -37, -57, -63, -27, -38,… $ beacons <int> 846, 750, 694, 510,
> 647, 251, 1647, 125… $ IV <int> 504, 116, 26, 21, 6, 3430, 80, 11, 0,
> 0… $ `LAN IP` <chr> “0. 0. 0. 0”, “0. 0. 0. 0”, “0. … $ `ID-length`
> <int> 12, 4, 2, 14, 25, 13, 12, 13, 24, 12, 1… $ ESSID <chr>”C322U13
> 3965”, “Cnet”, “KC”, “POCO X5 … $ Key <lgl> NA, NA, NA, NA, NA, NA,
> NA, NA, NA, NA,…

> glimpse(client_tidy) Rows: 12,081 Columns: 7 $ `Station MAC` <chr>
> “CA:66:3B:8F:56:DD”, “96:35:2D:3D:85:E6… $ `First time seen` <dttm>
> 2023-07-28 09:13:03, 2023-07-28 09:13:… $ `Last time seen` <dttm>
> 2023-07-28 10:59:44, 2023-07-28 09:13:… $ Power <int> -33, -65, -39,
> -61, -53, -43, -31, -71,… $ packets <int> 858, 4, 432, 958, 1, 344,
> 163, 3, 115, … $ BSSID <chr>”BE:F1:71:D5:17:8B”, “(not associated)”… $
> `Probed ESSIDs` <chr> “C322U13 3965”, “IT2 Wireless”, “C322U2…

## Анализ

# Точки доступа

1.  Определили небезопасные точки доступа (без шифрования – OPN)

> ap_tidy %\>% + filter(Privacy == “OPN”) %\>% + count() 1 42

1.  Определили производителя для каждого обнаруженного устройства
2.  Выявили устройства, использующие последнюю версию протокола
    шифрования WPA3, и названия точек доступа, реализованных на этих
    устройствах

> ap_tidy %\>% + filter(Authentication == “SAE PSK” | Privacy == “WPA3
> WPA2”) %\>% + distinct(ESSID) %\>% + arrange(ESSID) %\>% print()
> ESSID  
> 1 “Christie’s”  
> 2 “iPhone (Анастасия)”  
> 3 “iPhone XS Max 001f98a001f431001f98a” 4 “Димасик”  
> 5 NA

1.  Отсортировали точки доступа по интервалу времени, в течение которого
    они находились на связи, по убыванию.

> ap_tidy %\>% + arrange(desc(Connection_duration)) %\>% print() \# A
> tibble: 167 × 17 BSSID `First time seen` `Last time seen` channel
> Speed Privacy <chr> <dttm> <dttm> <int> <dbl> <chr>  
> 1 00:2… 2023-07-28 09:13:06 2023-07-28 11:56:21 44 -1 OPN  
> 2 E8:2… 2023-07-28 09:13:09 2023-07-28 11:56:05 11 130 OPN  
> 3 E8:2… 2023-07-28 09:13:03 2023-07-28 11:55:38 6 130 OPN  
> 4 08:3… 2023-07-28 09:13:27 2023-07-28 11:55:53 14 -1 WPA  
> 5 6E:C… 2023-07-28 09:13:03 2023-07-28 11:55:12 1 130 WPA2  
> 6 E8:2… 2023-07-28 09:13:06 2023-07-28 11:55:12 6 130 OPN  
> 7 E8:2… 2023-07-28 09:13:06 2023-07-28 11:55:11 6 130 OPN  
> 8 48:5… 2023-07-28 09:13:06 2023-07-28 11:55:11 1 270 WPA2  
> 9 E8:2… 2023-07-28 09:13:06 2023-07-28 11:55:10 6 -1 OPN  
> 10 8E:5… 2023-07-28 09:13:06 2023-07-28 11:55:09 6 65 WPA2

1.  Обнаружили топ-10 самых быстрых точек доступа.

> ap_tidy %\>% + arrange(desc(Speed)) %\>% + select(BSSID, ESSID, Speed)
> %\>% + head(10) BSSID ESSID Speed 1 26:20:53:0C:98:E8 NA 866 2
> 96:FF:FC:91:EF:64 NA 866 3 CE:48:E7:86:4E:33 iPhone (Анастасия) 866 4
> 8E:1F:94:96:DA:FD iPhone (Анастасия) 866 5 9A:75:A8:B9:04:1E KC 360 6
> 4A:EC:1E:DB:BF:95 POCO X5 Pro 5G 360 7 56:C5:2B:9F:84:90 OnePlus 6T
> 360 8 E8:28:C1:DC:B2:41 MIREA_GUESTS 360 9 E8:28:C1:DC:B2:40
> MIREA_HOTSPOT 360 10 E8:28:C1:DC:B2:42 NA 360

1.  Отсортировали точки доступа по частоте отправки запросов (beacons) в
    единицу времени по их убыванию

> ap_tidy %\>% + mutate(Beacon_rate = beacons / Connection_duration)
> %\>% + arrange(desc(Beacon_rate)) %\>% + select(BSSID, ESSID, beacons,
> Connection_duration, Beacon_rate) BSSID ESSID beacons
> Connection_duration Beacon_rate <chr> <chr> <int> <dbl> <dbl> 1
> 76:E4:ED:B0:5C:9A Инет от … 1 0 Inf 2 C2:B5:D7:7F:07:A8 DIRECT-a… 1 0
> Inf 3 E8:28:C1:DE:47:D1 NA 1 0 Inf 4 A2:FE:FF:B8:9B:C9 Christie… 1 0
> Inf 5 BA:2A:7A:DD:38:3E Айфон (O… 1 0 Inf 6 76:5E:F3:F9:A5:1C Redmi
> 9C… 1 0 Inf 7 00:03:7F:12:34:56 MT_FREE 1 0 Inf 8 E0:D9:E3:49:00:B1 NA
> 1 0 Inf 9 E8:28:C1:DC:BD:52 MIREA_HO… 1 0 Inf 10 00:26:CB:AA:62:72
> GIVC 1 0 Inf

# Данные клиентов

1.  Определить производителя для каждого обнаруженного устройства
2.  Обнаружить устройства, которые НЕ рандомизируют свой MAC адрес
3.  Кластеризовать запросы от устройств к точкам доступа по их именам.
    Определить время появления устройства в зоне радиовидимости и время
    выхода его из нее.

> client_tidy %\>% + filter(!is.na(`Probed ESSIDs`) & `Probed ESSIDs` !=
> ““) %\>% + select(`Station MAC`, `Probed ESSIDs`, `First time seen`,
> `Last time seen`, Power) %\>% + rename( + First_seen =
> `First time seen`, Last_seen = `Last time seen`, Signal_power = Power)
> `Station MAC` `Probed ESSIDs` First_seen  
> 1 CA:66:3B:8F:56:DD C322U13 3965 2023-07-28 09:13:03 2
> 96:35:2D:3D:85:E6 IT2 Wireless 2023-07-28 09:13:03 3 5C:3A:45:9E:1A:7B
> C322U21 0566 2023-07-28 09:13:03 4 C0:E4:34:D8:E7:E5 C322U13 3965
> 2023-07-28 09:13:03 5 68:54:5A:40:35:9E C322U06 5179,Galaxy A71
> 2023-07-28 09:13:06 6 CA:54:C4:8B:B5:3A GIVC 2023-07-28 09:13:06 7
> 4A:C9:28:46:EE:3F KOTIKI_XXX 2023-07-28 09:13:08 8 A0:E7:0B:AE:D5:44
> AndroidAP177B 2023-07-28 09:13:09 9 00:95:69:E7:7F:35 nvripcsuite
> 2023-07-28 09:13:11 10 00:95:69:E7:7C:ED nvripcsuite 2023-07-28
> 09:13:11

1.  Оценить стабильность уровня сигнала внури кластера во времени.
    Выявить наиболее стабильный кластер.
