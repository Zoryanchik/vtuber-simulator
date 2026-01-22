using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class HeadController : MonoBehaviour
{
    [Header("References")]
    public OSCReceiver oscReceiver;  
    public Transform headBone; // lnik to the head bone of the avatar     

    [Header("Rotation Settings")]
    [Range(0f, 90f)]
    [Tooltip("Maximum left/right turning angle")]
    public float maxHorizontalAngle = 30f;

    [Range(0f, 45f)]
    [Tooltip("Maximum up/down turning angle")]
    public float maxVerticalAngle = 20f;

    [Range(0f, 1f)]
    [Tooltip("Head turning speed (0.1 = smooth, 1 = fast)")]
    public float rotationSpeed = 0.15f;

    [Header("Inversion")]
    public bool invertHorizontal = false;
    public bool invertVertical = false;

    [Header("Debug")]
    public bool showDebugInfo = true;


    private Quaternion initialRotation;
    private Quaternion targetRotation;

    void Start()
    {
        if (oscReceiver == null)
        {
            Debug.LogError("OSCReceiver not assigned!");
            return;
        }

        if (headBone == null)
        {
            Debug.LogError("Head Bone not assigned!");
            return;
        }

        initialRotation = headBone.localRotation;
        targetRotation = initialRotation;

        Debug.Log("Head Controller initialized!");
        Debug.Log($"Head bone: {headBone.name}");
    }

    void Update()
    {
        if (oscReceiver == null || headBone == null)
            return;

        float headX = oscReceiver.headX;  
        float headY = oscReceiver.headY;  

        if (invertHorizontal) headX = -headX;
        if (invertVertical) headY = -headY;

        float yaw = headX * maxHorizontalAngle;    
        float pitch = headY * maxVerticalAngle;  

        targetRotation = initialRotation * Quaternion.Euler(pitch, yaw, 0f);

        // this is where the smoothing happens
        headBone.localRotation = Quaternion.Slerp(
            headBone.localRotation,
            targetRotation,
            rotationSpeed
        );
    }

    public void ResetHead()
    {
        if (headBone != null)
        {
            headBone.localRotation = initialRotation;
        }
    }

    void OnGUI()
    {
        if (!showDebugInfo) return;

        GUILayout.BeginArea(new Rect(10, 380, 300, 100));
        GUILayout.Label("=== Head Controller ===");

        if (headBone != null)
        {
            float headX = oscReceiver.headX;
            float headY = oscReceiver.headY;

            if (invertHorizontal) headX = -headX;
            if (invertVertical) headY = -headY;

            float yaw = headX * maxHorizontalAngle;
            float pitch = headY * maxVerticalAngle;

            GUILayout.Label($"Yaw (Y): {yaw:F1}°");
            GUILayout.Label($"Pitch (X): {pitch:F1}°");
        }

        GUILayout.EndArea();
    }
}
