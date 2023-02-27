import axios from "axios";
import { LoginModel, UserModel } from "../models/login.models";

const authUser = {
    loginUser(user: LoginModel) {
        return axios.post(
            "http://0.0.0.0:5001/auth",
            {
              username: user.username,
              password: user.password,
            }
          )

    }
}
export default authUser;
