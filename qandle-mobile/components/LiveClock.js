import React,{ useState, useEffect } from 'react';
import {Text, StyleSheet} from 'react-native';

const LiveClock = () => {
  const [currentTime, setCurrentTime] = useState('');
    useEffect(()=>{
        const timer=setTimeout(()=>{
            const now=new Date();
            const hours=now.getHours().toString().padStart(2,'0');
            const minutes=now.getMinutes().toString().padStart(2,'0');
            const seconds=now.getSeconds().toString().padStart(2,'0');
            setCurrentTime(`${hours}:${minutes}:${seconds}`);
        },1000);
        return()=>clearTimeout(timer);
    }, [currentTime]);
    return <Text style={styles.clockText}>{currentTime}</Text>
}
const styles=StyleSheet.create({
  clockText:{
    fontSize:20,
    fontWeight:'bold',
  }
})
export default LiveClock;