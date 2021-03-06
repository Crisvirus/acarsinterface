[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]




<!-- PROJECT LOGO -->
<br />
<p align="center">

  <h3 align="center">Acars Interface</h3>

  <p align="center">
    Web Interface for acarsdec
    <br />
  </p>
</p>


<!-- ABOUT THE PROJECT -->
## About The Project

This project is a webserver that displays data, captured with acarsdec, in a more friendly way. It groups the ACARS messages for each plane.
The main page displays all the planes captured in the last hour, with brief information about each of them.
![Acarsinterface main page][last_hour_index]

Each plane page has the same brief at the top, and a collection of cards. The first 3 are always present, and they show information that could be extracted from the ACARS messages. The rest of them are cards showing the messages received in the last 8 hours. There are 3 types of cards:

    * Text Message: The default card
    * Arinc 622 card: Shows the data in a JSON format
    * Route Card: Contains route infromation, usualy a list of waypoints separated by '.'
    * Takeoff clearance: A message that says to the pilot that they were cleared for takoff. It specifies the destination, takoff runway, and the navpoint that they have to follow. If the airport that sent the message is "Schiphol", I also added a link to the departure chart for the specified runway
    * Clearance Message: A message confirming that the pilots recieved the takeoff clearance

![Acarsinterface plane info][plane_info]

### Interface
#### Text Message Card
    This card is very simple. It shows the message, and a button labled "Expand". The button opens a modal that shows the entire message as it was received.

#### Arinc 622 Message Card
    It shows the text of the message and an "Expand" button. The button opens a modal that shows the data contained in the message, in a JSON format.

#### Clearance Message
    It shows the message, and a button labled "Expand". The button opens a modal that shows the entire message as it was received. The difference between this and the Text Message Card is the color.

#### Takeoff Clearance Message Card
    It shows the message, a section with extracted information (the runway, destination and waypoint),a button labled "Open Runway Chart" and a button labled "Expand". The "Open Runway Chart" opens a pdf with the departure chart for the specified runway (Only works for Schiphol Airport). The "Expand" button opens a modal that shows the entire message as it was received.

#### Route Message Card
    It shows the text and the "Expand" button. The diference is the "Open Route" button. This opens a new page with a list of waypoint separated by spaces. Use the "Copy to clipboard" button so save the list, and the use the "Go to Skyvector" to open https://skyvector.com/. On the top left, press the "Flight Plan button" and paste the waypoints in the text box.

### Built With

* [Python](https://www.python.org/)
* [My fork of acarsdec](https://github.com/Crisvirus/acarsdec)
* [libacars](https://github.com/szpajder/libacars)
* [Bootstrap](https://getbootstrap.com)
* [JQuery](https://jquery.com)
* [Jinja](https://jinja.palletsprojects.com/en/2.11.x/)




<!-- GETTING STARTED -->
## Getting Started
For my project I had to add another field to the JSON output of acarsdec. This is why my fork of acarsdec is needed.
### Prerequisites

The folowing are needed for this project to work
* Python 3: I made the project using Python 3.8.5, but it could work with older versions, but it must be Python 3
* libacars - follow the instruction from here : https://github.com/szpajder/libacars
* acarsdec - my fork of acarsdec is needed for now, follow installation instructions from there : https://github.com/Crisvirus/acarsdec
* Jinja, bcrypt, tinyDB -
  ```sh
  pip3 install Jinja2
  pip3 install bcrypt
  pip3 install tinyDB
  ```

### Installation

1. It's written in Python, so no installation required, just clone the repo and create the password database
```sh
git clone https://github.com/Crisvirus/acarsinterface
cd acarsinterface
mkdir passwordDB
```
2. (Optional) If you want to use HTTPS, obtain a certificate (ex: from [Let's Encrypt](https://letsencrypt.org/))
3. (Optional) Create the certs directory
```sh
mkdir certs
```
4. (Optional) Copy the certificates to the "certs" directory.

<!-- USAGE EXAMPLES -->
## Usage

1. First, start the server using 
```sh
python3 server.py
```

2. Start acarsdec. You can run acarsdec on the same machine, or on any machine that can reach the server
```sh
acarsdec -j <ip-of-the-server>:5555 -r 0 131.550 131.525 131.725 131.850 131.825
```
The frequencies used are an example for Europe. For other areas search online for the usually used ACARS frequencies.

<!-- 3. (Optional) The waypoints database is saved in the folder ./waypointsDB/CSVData/ . The information is taken from "http://navaid.com/GPX/" in gpx format. The script "./waypointsDB/convert.py" reads all the files from the folder ./waypointsDB/GPXData/ and converts them to csv, saving only the information that is needed. The GPX file is aprox. 50MB, so I didn't upload it to github. If you want to update the waypoint information, go to "http://navaid.com/GPX/" and download the data in ./waypointsDB/GPXData/. Then run:
```sh
cd waypointDB
python3 convert.py
```
This operation will take a while, and can use a lot of memory (in my case it used over 1GB of RAM), so only run it on a computer, not on a Raspberry. -->

<!-- ROADMAP -->
## Roadmap
Features that are on the TODO list:

    * More types of messages with more information extracted from the text



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Project Link: [https://github.com/Crisvirus/acarsinterface](https://github.com/Crisvirus/acarsinterface)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [acarsdec](https://github.com/TLeconte/acarsdec)
* [libacars](https://github.com/szpajder/libacars)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Crisvirus/acarsinterface.svg?style=for-the-badge
[contributors-url]: https://github.com/Crisvirus/acarsinterface/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Crisvirus/acarsinterface.svg?style=for-the-badge
[forks-url]: https://github.com/Crisvirus/acarsinterface/network/members
[stars-shield]: https://img.shields.io/github/stars/Crisvirus/acarsinterface.svg?style=for-the-badge
[stars-url]: https://github.com/Crisvirus/acarsinterface/stargazers
[issues-shield]: https://img.shields.io/github/issues/Crisvirus/acarsinterface.svg?style=for-the-badge
[issues-url]: https://github.com/Crisvirus/acarsinterface/issues
[license-shield]: https://img.shields.io/github/license/Crisvirus/acarsinterface.svg?style=for-the-badge
[license-url]: https://github.com/Crisvirus/acarsinterface/blob/master/LICENSE.txt
[last_hour_index]: images/last_hour_index.jpg
[plane_info]: images/plane_info.jpg
