// DEMONSTRATION ONLY: no real donor information.
// Use the Firebase modular browser SDK on a trusted HTTPS deployment.
import { initializeApp } from 'https://www.gstatic.com/firebasejs/11.10.0/firebase-app.js';
import { getAuth, signInWithEmailAndPassword, signOut, setPersistence, browserSessionPersistence } from 'https://www.gstatic.com/firebasejs/11.10.0/firebase-auth.js';
import { getFirestore, collection, addDoc, getDocs, updateDoc, doc, serverTimestamp } from 'https://www.gstatic.com/firebasejs/11.10.0/firebase-firestore.js';

export async function connect(config) {
  if (!config?.apiKey || !config?.projectId || !config?.authDomain || !config?.appId) throw new Error('Firebase web app configuration required');
  const app = initializeApp(config);
  const auth = getAuth(app);
  await setPersistence(auth, browserSessionPersistence);
  const db = getFirestore(app); // memory cache; persistent offline storage is not enabled
  const ensureSignedIn = () => { if (!auth.currentUser) throw new Error('Staff sign-in required'); };
  return {
    auth,
    signIn: (email,password) => signInWithEmailAndPassword(auth,email,password),
    signOut: () => signOut(auth),
    async saveReviewed(fields) {
      ensureSignedIn();
      const allowed = ['name','age','phone','city','donation','notes'];
      const clean = Object.fromEntries(allowed.map(k => [k, String(fields[k] ?? '').trim().slice(0,500)]));
      if (!Object.values(clean).some(Boolean)) throw new Error('Enter a demo field first');
      const ref = await addDoc(collection(db,'demo_records'), {fields:clean,source:'manual_review',status:'reviewed',reviewerUid:auth.currentUser.uid,createdAt:serverTimestamp()});
      return ref.id;
    },
    async listReviewed() {
      ensureSignedIn();
      const snapshot=await getDocs(collection(db,'demo_records'));
      return snapshot.docs.map(item=>({id:item.id,...item.data()}));
    },
    async updateNotes(id,notes){
      ensureSignedIn();
      await updateDoc(doc(db,'demo_records',id),{'fields.notes':String(notes).slice(0,500)});
    }
  };
}
