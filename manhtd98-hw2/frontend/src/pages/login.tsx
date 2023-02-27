import React from 'react';
import { Button, Checkbox, Form, Input } from 'antd';
import { LoginModel, UserModel } from '../models/login.models';
import authUser from '../hook/login';

const onFinish = (values: LoginModel) => {

  var loginAuth = authUser.loginUser(values).then(
    response =>{
      if (response.data.length >0){
        
      }else{
        console.log("Authentication Fail");
      }
    }
  ).catch(
    error => console.log(error)
  )

  console.log('Success:', loginAuth);
};

const App: React.FC = () => (
  <Form
    name="basic"
    labelCol={{ span: 8 }}
    wrapperCol={{ span: 16 }}
    style={{ maxWidth: 600 }}
    initialValues={{ remember: true }}
    onFinish={onFinish}
    // onFinishFailed={onFinishFailed}
    autoComplete="off"
  >
    <Form.Item
      label="Username"
      name="username"
      rules={[{ required: true, message: 'Please input your username!' }]}
    >
      <Input />
    </Form.Item>

    <Form.Item
      label="Password"
      name="password"
      rules={[{ required: true, message: 'Please input your password!' }]}
    >
      <Input.Password />
    </Form.Item>

    <Form.Item name="remember" valuePropName="checked" wrapperCol={{ offset: 8, span: 16 }}>
      <Checkbox>Remember me</Checkbox>
    </Form.Item>

    <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
      <Button type="primary" htmlType="submit">
        Submit
      </Button>
    </Form.Item>
  </Form>
);

export default App;

