# 🩺 LifeLink — AI-Powered Emergency Healthcare Platform

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Flask](https://img.shields.io/badge/Flask-Backend-red)
![Firebase](https://img.shields.io/badge/Firebase-Realtime-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active%20Development-brightgreen)

> **Saving minutes. Saving lives.**

**LifeLink** is a unified, AI-powered emergency healthcare platform that connects **citizens, hospitals, blood banks, organ donors, and ambulance services** in real time.  
It provides **separate interfaces for Users and Hospitals**, enabling faster coordination, predictive emergency response, and centralized life-saving data.

---

## 📸 Screenshots

### 🧭 User Dashboard


### 🚨 Emergency SOS


### 🏥 Hospital Dashboard


### 🩸 Blood & 🫀 Organ Databases


### 🧠 AI Health Intelligence


> 📂 Place all images inside a `/screenshots` folder.

---

## 🚑 Why LifeLink?

Emergency healthcare often fails due to:
- Fragmented blood & organ availability data
- Manual hospital coordination
- Delayed ambulance dispatch
- No early warning before emergencies

**LifeLink solves this by acting as a real-time digital bridge between users and hospitals.**

---

## 👤 User Interface Features

### 🚨 Emergency SOS
- One-tap emergency trigger
- Sends live location & medical profile
- Notifies hospitals and ambulances instantly

### 🩸 Blood Database
- Search blood groups
- Locate nearby compatible donors
- Real-time availability across hospitals

### 🫀 Organ Availability
- View organ stock and priority queues
- Receive alerts for potential matches

### 🧠 AI Health Intelligence
- Risk scoring & health predictions
- Emergency severity analysis

### 💊 Rare Medicine & Anti-venom
- Discover critical drugs
- See hospital stock locations

### 👥 Support & Future Donors
- Manage emergency contacts
- Donor pledges and future planning

---

## 🏥 Hospital Interface Features

### 🏥 Hospital Dashboard
A dedicated control panel for hospitals to manage all emergency resources.

### 🩸 Blood Database Management
- Add / update blood units
- Track availability in real time

### 🫀 Organ Database
- Update organ stock
- Manage recipient priority queues

### 💊 Drug & Inventory Management
- Rare medicines
- Anti-venoms
- Critical hospital supplies

### 📅 Appointment & Doctor Scheduling
- Manage appointments
- Doctor availability tracking

### 👩‍⚕️ Nurse Scheduler
- Assign nurses
- Track duty rotations

### 🚑 Ambulance Management
- Track hospital ambulances
- Monitor dispatch & availability

---

## 📊 System Architecture

```text
            USER APP / WEB
                   │
                   ▼
           Frontend (HTML/CSS/JS)
                   │
                   ▼
              Flask API Layer
                   │
   ┌───────────────┼────────────────┐
   │               │                │
AI Triage     Hospital Services   Emergency Logic
   │               │                │
   └───────────────┴────────────────┘
                   │
                   ▼
          Firebase Realtime Database
                   │
     ┌─────────────┼─────────────┐
     │             │             │
 Users        Hospitals      Ambulances
