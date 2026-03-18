import React, { useState } from 'react';
import { View, Text, TextInput, StyleSheet } from 'react-native';
import { Button } from 'react-native-elements';
import { Picker } from '@react-native-picker/picker';

const Registration = () => {
  const [name, setName] = useState('');
  const [employeeCode, setEmployeeCode] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [time, setTime] = useState('18:00');
  const [reason, setReason] = useState('');

  return (
    <View style={{ flex: 1, padding: 20, backgroundColor: 'lightblue' }}>
      <Text style={{ fontSize: 24, marginBottom: 20 }}>Registration</Text>

      <Text>Name</Text>
      <TextInput
        value={name}
        onChangeText={setName}
        placeholder="Enter your name"
        style={styles.input}
      />

      <Text>Employee Code</Text>
      <TextInput
        value={employeeCode}
        onChangeText={setEmployeeCode}
        placeholder="Enter employee code"
        style={styles.input}
      />

      <Text>Email</Text>
      <TextInput
        value={email}
        onChangeText={setEmail}
        placeholder="Enter email"
        keyboardType="email-address"    // shows @ key on keyboard
        style={styles.input}
      />

      <Text>Password</Text>
      <TextInput
        value={password}
        onChangeText={setPassword}
        placeholder="Enter password"
        secureTextEntry={true}          // hides the text like ••••
        style={styles.input}
      />
  <Text>Reason</Text>
      <TextInput
        value={reason}
        onChangeText={setReason}
        placeholder="Enter reason"
        style={styles.input}
      />
        
      <Text>Preferred Time</Text>
      <Picker
        selectedValue={time}
        onValueChange={(val) => setTime(val)}
        style={{ backgroundColor: 'white', marginTop: 5 }}
      >
        <Picker.Item label="6:00 PM" value="18:00" />
        <Picker.Item label="6:30 PM" value="18:30" />
        <Picker.Item label="7:00 PM" value="19:00" />
        <Picker.Item label="7:30 PM" value="19:30" />
        <Picker.Item label="8:00 PM" value="20:00" />
      </Picker>

      <Button
        title="Register"
        buttonStyle={{ marginTop: 20, backgroundColor: 'blue' }}
        onPress={() => {
          // later: send data to backend
          console.log({ name, employeeCode, email, password, time });
        }}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  input: {
    height: 40,
    backgroundColor: 'white',
    marginTop: 5,
    marginBottom: 15,
    paddingHorizontal: 10,
    borderRadius: 5,
  },
});

export default Registration;
