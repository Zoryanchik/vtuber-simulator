using UnityEngine;
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;


public class OSCReceiver : MonoBehaviour
{
    [Header("Network Settings")]
    public int port = 5005;

    [Header("Received Data")]
    public float mouthOpen = 0f;
    public float eyeLeft = 1f;
    public float eyeRight = 1f;
    public float headX = 0f;
    public float headY = 0f;

    private UdpClient udpClient;
    private Thread receiveThread;
    private bool isRunning = false;

    void Start()
    {
        // Initialize UDP client
        isRunning = true;
        receiveThread = new Thread(ReceiveData);
        receiveThread.Start();
        receiveThread.IsBackground = true;

        Debug.Log("OSC Receiver started on port " + port);
    }

    void ReceiveData()
    {
        udpClient = new UdpClient(port);

        while (isRunning)
        {
            try
            {
                IPEndPoint remoteEndPoint = new IPEndPoint(IPAddress.Any, port);
                byte[] data = udpClient.Receive(ref remoteEndPoint);
                ParseOSCMessage(data);
            }
            catch (Exception ex)
            {
                Debug.LogError("Error receiving data: " + ex.Message);
            }
        }
    }
    void ParseOSCMessage(byte[] data)
    {
        //Osc message format: address (string) + value (float)
        string message = Encoding.ASCII.GetString(data);

        // Last 4 data
        float value = ExtractFloat(data);
        if (message.Contains("/face/mouth"))
        {
            mouthOpen = value;
        }
        else if (message.Contains("/face/eye_left"))
        {
            eyeLeft = value;
        }
        else if (message.Contains("/face/eye_right"))
        {
            eyeRight = value;
        }
        else if (message.Contains("/face/head_x"))
        {
            headX = value;
        }
        else if (message.Contains("/face/head_y"))
        {
            headY = value;
        }
    }

    float ExtractFloat(byte[] data)
    {
        if (data.Length < 4) return 0f;

        int startIndex = data.Length - 4;

        // big -endian to little-endian conversion
        byte[] floatBytes = new byte[4];
        floatBytes[0] = data[startIndex + 3];
        floatBytes[1] = data[startIndex + 2];
        floatBytes[2] = data[startIndex + 1];
        floatBytes[3] = data[startIndex];

        return BitConverter.ToSingle(floatBytes, 0);
    }


}