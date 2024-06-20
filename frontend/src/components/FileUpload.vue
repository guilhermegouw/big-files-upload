<template>
    <div>
        <input type="file" @change="handleFileUpload" />
        <button @click="submitFile">Upload!</button>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        data() {
            return {
                file: null
            };
        },
        methods: {
            handleFileUpload(event) {
                this.file = event.target.files[0];
            },
            async submitFile() {
                if (!this.file) {
                    alert('Please select a file');
                    return;
                }
                try {
                    const fileName = this.file.name;
                    const contentType = this.file.type;

                    const response = await axios.post('http://localhost:8000/api/generate-signed-url/', {
                        file_name: fileName,
                        content_type: contentType
                    });

                    console.log('Signed URL response:', response.data);

                    const { url } = response.data;

                    await axios.put(url, this.file, {
                        headers: {
                            'Content-Type': contentType
                        }
                    });

                    alert('File uploaded successfully');
                } catch (error) {
                    alert('An error occurred while uploading the file');
                    console.error('Error uploading file', error);
                }
            }
        }
    };
</script>

