
class Token {
    get() {
        const token = localStorage.getItem("token");

        return token;
    }

    set(token) {
        localStorage.setItem("token", token);
    }
}

export default Token;