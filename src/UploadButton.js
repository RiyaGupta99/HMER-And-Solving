import React, { Component } from 'react';
import { Button, Modal, Image, Alert } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

let imgBase64 = '';

class UploadButton extends Component {
    constructor(props) {
        super(props);
        this.state = {
            uploadState: true,
            imgUrl: '',
            uploadError: false,
            showModal: false
        };
    }

    validateFile = (event) => {
        let extension = event.target.files[0].name.substring(event.target.files[0].name.lastIndexOf('.') + 1).toLowerCase();
        let fileName = event.target.files[0].name;
        let img = '';
        if (extension === 'jpg' || extension === 'png' || extension === 'jpeg') {
            img = URL.createObjectURL(event.target.files[0]);
            let file = event.target.files[0];
            let reader = new FileReader();
            reader.onloadend = () => {
                imgBase64 = reader.result;
                this.setState(Object.assign(this.state, {
                    uploadState: false,
                    imgUrl: img,
                    uploadError: false,
                    showModal: true
                }));
                this.props.setUploadedImage(imgBase64);
                this.props.setUploadedImageName(fileName);
            }
            reader.readAsDataURL(file);
        }
        else {
            imgBase64 = '';
            this.setState(Object.assign(this.state, {
                uploadState: true,
                imgUrl: '',
                uploadError: true,
                showModal: true
            }));
            this.props.setUploadedImage(null);
            this.props.setUploadedImageName('');
        }
    }

    handleClose = () => {
        this.setState(Object.assign(this.state, { showModal: false }));
    }

    removeUploadedImage = () => {
        this.props.setUploadedImage(null);
        this.props.setUploadedImageName('');
        this.setState({
            uploadState: true,
            imgUrl: '',
            uploadError: false,
            showModal: false
        })
    }

    modalBody = () => {
        if (!this.state.uploadError) {
            return (
                <div>
                    <Image alt="selected image" src={this.props.uploadedImage} fluid />
                </div>
            );
        }
        else {
            return (
                <div>
                    <Alert variant="danger">
                        The selected file is not an image. Please select an image
                    </Alert>
                </div>
            );
        }
    }

    render() {
        return (
            <div>
                <div>
                    <input type="file" onChange={this.validateFile} style={{"marginBottom": "2%"}}/>
                </div>
                <div style={{"marginBottom": "5%"}}>
                    <button disabled={this.props.uploadedImage === null} className="btn btn-primary btn-block" type="button" onClick={() => this.setState({ showModal: !this.state.showModal })}>Preview</button>
                    <button disabled={this.props.disable} className="btn btn-primary btn-block" type="button" onClick={this.removeUploadedImage}>Remove</button>
                </div>
                <Modal
                    show={this.state.showModal}
                    onHide={this.handleClose}
                    size="lg"
                    aria-labelledby="contained-modal-title-vcenter"
                >
                    <Modal.Header closeButton>
                        <Modal.Title>
                            {this.state.uploadError ? "Error in extension" : "Preview of selected image"}
                        </Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        {this.modalBody()}
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant="secondary" onClick={this.handleClose}>
                            Close
                        </Button>
                    </Modal.Footer>
                </Modal>
            </div>
        );
    }
}

export default UploadButton;
