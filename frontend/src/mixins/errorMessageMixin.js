import { ref } from 'vue'
export default {
    setup() {
        let errorMessage = ref('')
        return { errorMessage }
    },
    methods: {
        clearMessage() {
            this.errorMessage = ''
        }
    }
}
