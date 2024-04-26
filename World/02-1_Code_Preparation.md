# Required files

To perform oxide and valence determination from raw data, the following files are required.

+ Raw Data (.txt file)
+ Detailed information about XAS analysis (.tsv file)

Please make sure to individually assign a data identification number at the beginning of the file name. 

For example, instead of naming it A.txt / A.tsv, name it **001_A.txt / 001_A.tsv**, and so on.

## Raw Data (.txt file)
+ The first column is **X-ray energy** (horizontal axis of the spectrum)
+ The second column is **Absorption coefficient** (vertical axis of the spectrum))
> [!NOTE]
> The absorption coefficient can be either normalized or unnormalized.

![rawdata](/World/RawData_txtfile.png)

>
> [!NOTE]
> If raw data is **9809 format**, please utilize the following code.
>
> The 9809 format is one of the measurement data formats output by the XAFS measurement program developed by Dr. Nomura, who oversees the XAFS beamlines at KEK PF, specifically for use on the XAFS beamlines at Photon Factory (Tsukuba, Japan).
>
> In 9809 format, the X-ray energy corresponds to **spectrometer angle**, <br>and the absorption coefficient corresponds to **the values of incident and transmitted light** (i.e., before calculating the absorption coefficient).
>
> Please refer to the following link for a detailed explanation of the 9809 format: <br>http://titan.nusr.nagoya-u.ac.jp/Tabuchi/BL5S1/doku.php/tabuchi/9809format



## Detailed information about XAS analysis (.tsv file)
+ At least, ensure that it contains **pairs of elements being analyzed and absorption edge names** and **the expected material name**.

![tsvdata](/World/Detailed_Information_tsvfile.png)

> [!NOTE]
> Above the case,
> + pairs of elements being analyzed → Ni (line 25)
> + absorption edge names → K-edge (line 25)
> + expected material name → NiO (line 16)
>
> The contents of the tsv file likely vary depending on the measurement facility. 
>
> However, these essential pieces of information should be included.
>
> The numbering of the codes to be introduced in the next part should be changed based on the lines containing the three items of information.
