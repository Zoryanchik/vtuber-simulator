using UnityEngine;

public class FaceAnimator : MonoBehaviour
{
    [Header("References")]
    public OSCReceiver oscReceiver;  
    public SkinnedMeshRenderer faceRenderer;

    [Header("BlendShape Names")]
    [Tooltip("For mouth")]
    public string mouthBlendShapeName = "A";

    [Tooltip("For left eye")]
    public string blinkLeftBlendShapeName = "Blink_L";

    [Tooltip("For right eye")]
    public string blinkRightBlendShapeName = "Blink_R";

    [Tooltip("For happy emotion")]
    public string happyBlendShapeName = "Joy";

    [Header("Settings")]
    [Range(0f, 200f)]
    [Tooltip("Multiplier for mouth opening intensity")]
    public float mouthMultiplier = 100f;

    [Range(0f, 200f)]
    [Tooltip("Multiplier for eye blinking intensity")]
    public float eyeMultiplier = 100f;

    [Range(0f, 200f)]
    [Tooltip("Multiplier for emotion intensity")]
    public float emotionMultiplier = 100f;

    [Header("Debug")]
    public bool showDebugInfo = true;


    private int mouthIndex = -1;
    private int blinkLeftIndex = -1;
    private int blinkRightIndex = -1;
    private int happyIndex = -1;

    void Start()
    {
        if (oscReceiver == null)
        {
            Debug.LogError("OSCReceiver not assigned!");
            return;
        }

        if (faceRenderer == null)
        {
            Debug.LogError("FaceRenderer not assigned!");
            return;
        }

        
        FindBlendShapeIndices();
    }

    void FindBlendShapeIndices()
    {
  
        Mesh mesh = faceRenderer.sharedMesh;

        if (mesh == null)
        {
            Debug.LogError("Mesh not found!");
            return;
        }

        // Looking for indexes
        mouthIndex = mesh.GetBlendShapeIndex(mouthBlendShapeName);
        blinkLeftIndex = mesh.GetBlendShapeIndex(blinkLeftBlendShapeName);
        blinkRightIndex = mesh.GetBlendShapeIndex(blinkRightBlendShapeName);
        happyIndex = mesh.GetBlendShapeIndex(happyBlendShapeName);

        Debug.Log("=== BlendShape Indices ===");
        Debug.Log($"Mouth '{mouthBlendShapeName}': {mouthIndex}");
        Debug.Log($"Blink Left '{blinkLeftBlendShapeName}': {blinkLeftIndex}");
        Debug.Log($"Blink Right '{blinkRightBlendShapeName}': {blinkRightIndex}");
        Debug.Log($"Happy '{happyBlendShapeName}': {happyIndex}");

        if (mouthIndex == -1)
            Debug.LogWarning($"Mouth blendshape '{mouthBlendShapeName}' not found!");
        if (blinkLeftIndex == -1)
            Debug.LogWarning($"Blink Left blendshape '{blinkLeftBlendShapeName}' not found!");
        if (blinkRightIndex == -1)
            Debug.LogWarning($"Blink Right blendshape '{blinkRightBlendShapeName}' not found!");
        if (happyIndex == -1)
            Debug.LogWarning($"Happy blendshape '{happyBlendShapeName}' not found!");
    }

    void Update()
    {
        if (oscReceiver == null || faceRenderer == null)
            return;

        if (mouthIndex >= 0)
        {
            float mouthValue = oscReceiver.mouthOpen * mouthMultiplier;
            faceRenderer.SetBlendShapeWeight(mouthIndex, mouthValue);
            if (showDebugInfo)
                Debug.Log($"Mouth Open: {mouthValue}");
        }
        if (blinkLeftIndex >= 0)
        {
            float eyeLeftValue = oscReceiver.eyeLeft * eyeMultiplier;
            faceRenderer.SetBlendShapeWeight(blinkLeftIndex, eyeLeftValue);
            if (showDebugInfo)
                Debug.Log($"Eye Left: {eyeLeftValue}");
        }
        if (blinkRightIndex >= 0)
        {
            float eyeRightValue = oscReceiver.eyeRight * eyeMultiplier;
            faceRenderer.SetBlendShapeWeight(blinkRightIndex, eyeRightValue);
            if (showDebugInfo)
                Debug.Log($"Eye Right: {eyeRightValue}");
        }
        if (happyIndex >= 0)
        {
            float happyValue = oscReceiver.happy * emotionMultiplier;
            faceRenderer.SetBlendShapeWeight(happyIndex, happyValue);
            if (showDebugInfo)
                Debug.Log($"Happy: {happyValue}");
        }
    }

    void OnGUI()
    {
        if (!showDebugInfo)
            return;
        GUILayout.BeginArea(new Rect(10, 220, 300, 150));
        GUILayout.Label("=== Face Animator ===");

        if (mouthIndex >= 0)
        {
            float mouthValue = oscReceiver.mouthOpen * mouthMultiplier;
            GUILayout.Label($"Mouth BlendShape: {mouthValue:F1}");
        }

        if (blinkLeftIndex >= 0)
        {
            float blinkValue = (1f - oscReceiver.eyeLeft) * eyeMultiplier;
            GUILayout.Label($"Blink L BlendShape: {blinkValue:F1}");
        }

        if (blinkRightIndex >= 0)
        {
            float blinkValue = (1f - oscReceiver.eyeRight) * eyeMultiplier;
            GUILayout.Label($"Blink R BlendShape: {blinkValue:F1}");
        }
        if (happyIndex >= 0)
        {
            float happyValue = oscReceiver.happy * emotionMultiplier;
            GUILayout.Label($"Happy BlendShape: {happyValue:F1}");
        }

        GUILayout.EndArea();
    }
}