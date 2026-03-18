import React from 'react'
import { useState } from 'react';
import { View, Text, TextInput, StyleSheet, Pressable } from 'react-native'
import { Picker } from '@react-native-picker/picker';
import { Button, Icon } from 'react-native-elements';
import LiveClock from '../../components/LiveClock';
import { router } from 'expo-router'
const Main = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [status, setStatus] = useState('Pending');
  const [time, setTime] = useState('18:30');
  const [reason, setReason] = useState('Client meeting');
  //this will be coming fomr backend
  const User = 'yashhh'
  const EmpCode = '12345'
  return (
    <View style={{ flex: 1 ,backgroundColor:'lightblue',alignItems: 'center' }}>
      <View style={styles.container}>
        <View style={styles.box}>
          <Icon
            name="menu"
            type='material'
            size={40}
            onPress={() => {
              setSidebarOpen(true);
            }}
            containerStyle={styles.iconContainer}
          />
          <LiveClock />
        </View>
      </View>
        
      <View style={styles.introBox}>
        <Text style={styles.introText}>Hi,{User}</Text>
        <Text style={styles.introText}>Employee Codee: {EmpCode}</Text>
      </View>
      {/* Overlay + Sidebar -> only when open */}
      {sidebarOpen && (
        <>
          <Pressable
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              backgroundColor: 'pink',
            }}
            onPress={() => setSidebarOpen(false)}
          />
          {/* Sidebar panel */}

          <View style={{ width: '70%', backgroundColor: 'white', top: 0, bottom: 0, left: 0, position: 'absolute' }}>
            <Pressable onPress={() => {
              router.push('/registration');
              setSidebarOpen(false);
            }}>
              <Text style={{ paddingTop: 40, paddingLeft: 20, marginTop: 30, alignItems: 'center', justifyContent: 'center' ,borderColor:'black', borderWidth:1}}>Register</Text>
            </Pressable>
            <Pressable onPress={() => { /* navigate somewhere else */ }}>
              <Text style={{ paddingTop: 40, paddingLeft: 20, alignItems: 'center', justifyContent: 'center' ,borderColor:'black', borderWidth:1}}>Settings</Text>
            </Pressable>
          </View>

        </>
      )}

      <View style={{ backgroundColor: 'pink', height: 100, width: 300, alignItems: 'center' }}>
        <Text style={{ color: 'white', marginTop: 10, fontSize: 20 }}>
          Today's Status
        </Text>
        <Text style={{ marginTop: 10, fontSize: 20 }}>Status:{status}</Text>
      </View>



      <View style={{ backgroundColor: 'red', height: 300, width: 300, alignItems: 'center', marginTop: 20 }}>
        <Text style={{ color: 'white', marginTop: 10, fontSize: 20 }}>
          OD regularization
        </Text>

        <Text style={{ marginTop: 10, fontSize: 20 }}>Notification Time:</Text>
        <Picker
          selectedValue={time}
          onValueChange={(val: string) => setTime(val)}
          style={{ height: 50, width: 200, backgroundColor: 'white' ,marginTop: 10}}
        >
          <Picker.Item label="6:00 PM" value="18:00" />
          <Picker.Item label="6:30 PM" value="18:30" />
          <Picker.Item label="7:00 PM" value="19:00" />
          <Picker.Item label="7:30 PM" value="19:30" />
          <Picker.Item label="8:00 PM" value="20:00" />
        </Picker>
        <Text style={{ marginTop: 10, fontSize: 20 }}>Defaultttt reason:</Text>
        <TextInput
          value={reason}
          onChangeText={setReason}
          style={{ height: 40, width: 200, backgroundColor: 'white', marginTop: 10, paddingHorizontal: 10, borderRadius: 5 }}
        />
        <Button title="Register first" style={{ paddingTop: 10, marginTop: 10, width: 200 }} onPress={()=>{
          router.push('/registration')
        }}></Button>
      </View>
    </View>
  )
}

const styles = StyleSheet.create({
  container: {
    // flex: 1,
    flexDirection: 'row',
    height: 130,
    backgroundColor: 'blue',
    // justifyContent:'center',
    // alignItems:'center'
  },
  box: {
    borderWidth: 2,
    flex: 1,
    flexDirection: 'row',
    justifyContent: 'space-between',
    height: 70,
    width: 50,
    backgroundColor: 'red',
    alignItems: 'center',
    padding: 10,
    color: 'white',
    fontSize: 20
  },
  iconContainer: {
    marginLeft: 10,
    backgroundColor: 'orange',
    marginTop: 10, // Adjust positioning as needed
  },
  introBox: {
    color: 'white', fontSize: 20, padding: 10, margin: 10, borderRadius: 10, marginRight: 105, justifyContent: 'center', alignItems: 'center'
  },
  introText: {
    color: 'black', fontSize: 20
  }
})

export default Main