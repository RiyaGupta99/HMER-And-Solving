export default function sketch(p){
    let canvasObj;
    let b = 0.7;
    let h = 0.55;
    p.setup = () => {
        canvasObj = p.createCanvas(p.windowWidth * b, p.windowHeight * h);
    }

    p.draw = () => {}

    p.mouseDragged = () => {
        p.stroke(0);
        p.strokeWeight(3);
        p.line(p.mouseX, p.mouseY, p.pmouseX, p.pmouseY);
    }

    p.myCustomRedrawAccordingToNewPropsHandler = (props) => {
        if(props.evaluate) {
            if(canvasObj) {
                canvasObj.loadPixels();
                let data = canvasObj.canvas.toDataURL();
                props.callBack(data);
            }
        }
        if(props.color){
            p.background(255);
        }
    }

    p.windowResized = () => {
        p.resizeCanvas(p.windowWidth * b, p.windowHeight* h);
    }
}
