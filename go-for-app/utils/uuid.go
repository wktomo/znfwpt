package utils

import (
	"encoding/binary"
	"encoding/hex"
	"fmt"
	"math/rand"
	"net"
	"sync"
	"time"
)

type UUID struct {
	nodeID      [6]byte
	clockSeq    uint16
	lastTime    int64
	timeOffset  int64
	randSource  *rand.Rand
	lock        sync.Mutex
}

func NewUUID() (*UUID, error) {
	rand.Seed(time.Now().UnixNano())
	uuid := &UUID{
		clockSeq:   uint16(rand.Intn(1 << 14)),
		timeOffset: time.Now().UnixNano() / 100,
		randSource: rand.New(rand.NewSource(time.Now().UnixNano())),
	}

	mac, err := getMACAddress()
	if err != nil {
		uuid.nodeID = getRandomNodeID()
	} else {
		copy(uuid.nodeID[:], mac)
	}

	return uuid, nil
}

func getMACAddress() ([]byte, error) {
	interfaces, err := net.Interfaces()
	if err != nil {
		return nil, err
	}

	for _, iface := range interfaces {
		if iface.Flags&net.FlagUp == net.FlagUp && iface.Flags&net.FlagLoopback == 0 && len(iface.HardwareAddr) > 0 {
			return iface.HardwareAddr, nil
		}
	}

	return nil, fmt.Errorf("no MAC address found")
}

func getRandomNodeID() [6]byte {
	nodeID := [6]byte{}
	for i := 0; i < 6; i++ {
		nodeID[i] = byte(rand.Intn(256))
	}
	return nodeID
}

func (u *UUID) Generate() string {
	u.lock.Lock()
	defer u.lock.Unlock()

	currentTime := time.Now().UnixNano() / 100

	if currentTime < u.lastTime {
		sleepDuration := time.Duration(u.lastTime - currentTime) * time.Nanosecond * 100
		time.Sleep(sleepDuration)
		currentTime = u.lastTime
	}

	timeLow := uint32(currentTime & 0xFFFFFFFF)
	timeMid := uint16((currentTime >> 32) & 0xFFFF)
	timeHiAndVersion := uint16((currentTime>>48)&0x0FFF) | 0x1000

	if currentTime == u.lastTime {
		u.clockSeq++
		if u.clockSeq == 0 {
			u.clockSeq = uint16(u.randSource.Int63n(1<<14))
		}
	} else {
		u.clockSeq = uint16(u.randSource.Int63n(1<<14))
	}

	clockSeqHiAndRes := uint16(u.clockSeq>>8) | 0x80
	clockSeqLow := uint8(u.clockSeq & 0xFF)

	uuidBytes := make([]byte, 16)
	binary.BigEndian.PutUint32(uuidBytes[0:4], timeLow)
	binary.BigEndian.PutUint16(uuidBytes[4:6], timeMid)
	binary.BigEndian.PutUint16(uuidBytes[6:8], timeHiAndVersion)
	uuidBytes[8] = byte(clockSeqHiAndRes)
	uuidBytes[9] = clockSeqLow
	copy(uuidBytes[10:16], u.nodeID[:])

	u.lastTime = currentTime

	return fmt.Sprintf("%x-%x-%x-%x-%x",
		uuidBytes[0:4],
		uuidBytes[4:6],
		uuidBytes[6:8],
		uuidBytes[8:10],
		uuidBytes[10:16])
}

func GenerateSimpleUUID() string {
	rand.Seed(time.Now().UnixNano())
	randomBytes := make([]byte, 16)
	rand.Read(randomBytes)
	return hex.EncodeToString(randomBytes)
}