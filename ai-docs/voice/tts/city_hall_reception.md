# City Hall Reception Call Handling

## Overview
This document details how the AI voice assistant handles incoming calls to Reykjavik City Hall's reception area, including standard greetings, call transfers, and follow-ups.

## Configuration

### Voice Settings
```yaml
voice:
  style: professional
  gender: female
  speaking_rate: 1.0
  language: is-IS
```

### XML Template
```xml
<LLAPSConfig>
    <Level1>
        <Role>System</Role>
        <Instruction>
            You are an AI phone assistant for Reykjavik City Hall, providing friendly, calm, and professional responses in Icelandic.
        </Instruction>
    </Level1>
    <Level2>
        <Role>Assistant</Role>
        <Prompt>
            Respond with a warm, friendly greeting in Icelandic, using a smooth, radio DJ-like voice.
        </Prompt>
    </Level2>
</LLAPSConfig>
```

## Usage Examples

### 1. Initial Greeting
```python
greeting = {
    "is": {
        "text": "Góðan daginn, þetta er Reykjavíkurborg. Hvernig get ég aðstoðað þig í dag?",
        "translation": "Good morning, this is Reykjavik City. How may I assist you today?"
    }
}
```

### 2. Hold Message
```python
hold_message = {
    "is": {
        "text": "Augnablik, ég kanna stöðuna og kem aftur til þín fljótlega. Vinsamlegast haltu á línunni.",
        "translation": "One moment, I'm checking the status and will be right back. Please stay on the line."
    }
}
```

## Integration Points

### Voice Processing
- Uses Azure Neural TTS for voice generation
- Implements custom voice style based on FM radio presenters
- Integrates with call handling system via WebSocket

### Call Flow
1. Incoming call detected
2. Initial greeting played
3. Speech-to-Text processes caller's request
4. AI determines appropriate response/action
5. Response generated and played
6. Call transferred or concluded as needed

## Notes

### Best Practices
- Keep initial greeting under 5 seconds
- Use consistent voice style throughout the call
- Maintain professional yet friendly tone
- Include clear action items in responses

### Common Issues
- Handle network latency in responses
- Manage background noise during calls
- Account for various Icelandic dialects
- Handle multiple concurrent calls efficiently

### Performance Metrics
- Response time: < 1.5 seconds
- Speech recognition accuracy: > 95%
- Call handling capacity: 50 concurrent calls
- User satisfaction rating: > 4.5/5

## Testing

### Test Cases
1. Basic greeting flow
2. Department transfer
3. Information requests
4. Emergency handling
5. Call conclusion

### Validation Steps
1. Voice quality check
2. Response timing measurement
3. Accent handling verification
4. Load testing under concurrent calls

## Maintenance

### Regular Updates
- Voice model fine-tuning
- Response template updates
- Performance optimization
- Log analysis and improvements

### Monitoring
- Track call success rates
- Monitor voice quality
- Analyze user satisfaction
- Review system performance