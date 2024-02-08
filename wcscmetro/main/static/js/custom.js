import chokidar from 'chokidar'

function carouselDetect() {
    var frame = document.getElementById('detect');
    
    if (isElementOnScreen(frame)) {
        console.log('The target div is on the screen!');
        // Do something when the div is on the screen
    } else {
        console.log('The target div is not on the screen.');
        // Do something else when the div is not on the screen
    }
}

function newAlerts() {
    const alpath = JSON.parse("filepath.json");
    const watcher = chokidar.watch(alpath.imapalerts);

    watcher
        .on('add' => {
            
        });

}