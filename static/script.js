//Temperature part

var temp;
var humi;

function GetWeatherForLocation() {
    document.getElementById('search').style.display = 'none';
    document.getElementById('getLocationButton').style.display = 'none';
    if ('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition(function (position) {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;

            fetch(`http://api.weatherstack.com/current?access_key=eace5001df19d0b57f6e7eb7634be99d&query=${latitude},${longitude}`)
                .then(response => response.json())
                .then(data => {
                    console.log('API Response:', data);
                    if (data.current) {
                        temp = data.current.temperature;
                        humi = data.current.humidity;
                        Predict(temp, humi);
                        document.getElementById("output").innerHTML = "Location: " + data.location.name + ". <br>Temperature: " + data.current.temperature + "°C. Humidity: " + data.current.humidity + ". Precipitation: " +data.current.precip + "<br>Description: " + data.current.weather_descriptions + ". And the cloud cover is " + data.current.cloudcover + "%";
                    } else {
                        document.getElementById("output").innerHTML = "Data not available for the specified location.";
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    document.getElementById("output").innerHTML = "Error fetching data.";
                });
        }, function (error) {
            console.error('Error getting location:', error);
            alert('Error getting location. Please check your device settings.');
        });
    } else {
        alert('Geolocation is not supported in your browser.');
    }
    var outputElement = document.getElementById("output");
    outputElement.style.fontSize = "23px";
}


function GetWeatherForCity() {
    document.getElementById('search').style.display = 'none';
    document.getElementById('getLocationButton').style.display = 'none';
    var city = document.getElementById("search").value;
    fetch(`http://api.weatherstack.com/current?access_key=eace5001df19d0b57f6e7eb7634be99d&query=${city}`)
        .then(response => response.json())
        .then(data => {
            console.log('API Response:', data);
            if (data.current) {
                temp = data.current.temperature;
                humi = data.current.humidity;
                Predict(temp, humi);
                document.getElementById("output").innerHTML = "Location: " + data.location.name + ". <br>Temperature: " + data.current.temperature + "°C. Humidity: " + data.current.humidity + ". Precipitation: " + data.current.precip + "<br>Description: " + data.current.weather_descriptions + ". And the cloud cover is " + data.current.cloudcover + "%";
            } else {
                document.getElementById("output").innerHTML = "Data not available for the specified location.";
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById("output").innerHTML = "Error fetching data.";
        });
    var outputElement = document.getElementById("output");
    outputElement.style.fontSize = "23px";
}

function Predict(temp, humi) {
    var diseaseElement = document.getElementById("DI");
    var disease = diseaseElement.textContent; 
    console.log("Disease Content: " + disease);   
    console.log("temp:" + temp);
    console.log("humi:" + humi);
    if(disease=="{{ prediction }}"){
        if(temp >= 20 && temp <= 29){
            if(humi >= 50){
                document.getElementById("POS").innerHTML = "Favorable conditions for spread";
                document.getElementById("ME").innerHTML = "Covering bunches with poly bags prior to monsoon were incorporated as a component in IDM of mahali. Prophylactic spraying of 1% Bordeaux mixture is effective in reducing the fungal population build up in monsoon season.";

            }
            else{
                document.getElementById("POS").innerHTML = "Unfavorable conditions for spread";
                document.getElementById("ME").innerHTML = "Not applicable";

            }
        }
        else{
            document.getElementById("POS").innerHTML = "Unfavorable conditions for spread";
            document.getElementById("ME").innerHTML = "Not applicable";

        } 
    }
}


//Image upload part

const dropArea = document.getElementById('drop-area');
const inputFile = document.getElementById('input-file');
const imageView = document.getElementById('img-view');

dropArea.addEventListener('dragover', (e) => {
    e.preventDefault();
});

dropArea.addEventListener('drop', (e) => {
    e.preventDefault();

    const droppedFile = e.dataTransfer.files[0];

    if (droppedFile && droppedFile.type.startsWith('image/')) {
        const imgLink = URL.createObjectURL(droppedFile);
        imageView.style.backgroundImage = `url(${imgLink})`;
        imageView.textContent = '';
        imageView.style.border = '0';
    } else {
        alert('Please drop an image file.');
    }
});

inputFile.addEventListener('change', uploadImage);

function uploadImage() {
    const imgLink = URL.createObjectURL(inputFile.files[0]);
    imageView.style.backgroundImage = `url(${imgLink})`;
    imageView.textContent = '';
    imageView.style.border = '0';

    
}
