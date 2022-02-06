import Dash from "dash";
import fs from "fs";
import { DAPI } from "./DAPI";

// wallet mnemonic to be used (we've used a mnemonic only, if you're using a passphrase that would have to be added)
// if you don't have one already: leave this empty, use createNewWallet() to create a new wallet and retrieve a funding address
const WALLET_MNEMONIC = "sure goat old tuna random width primary staff diary dove auto relax";
// identity key for the identity that is to be used, should have credits already!
const IDENTITY_ID = "8EJn4ZofkQxU5Ym9P4mKGUr74xaCoYgMn5t6ajo4tiZa";
// random prefix, can be anything
const PREFIX = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA";
// 5 digits for count suffix -> 34^5 options
const MAX_SUFFIX_LENGTH = 5;
// one digit for a machine id, required to allow multiple machines without a headache
const MACHINE_INFIX = "B";
// thread count, can be above actual cpu cores/vthreads, has to be <=34 however
const THREAD_COUNT = 2;

const Z_INDEX = "z".charCodeAt(0);
const A_INDEX = "a".charCodeAt(0);
const NINE_INDEX = "9".charCodeAt(0);
const ZERO_INDEX = "0".charCodeAt(0);

/*
** Generate new name suffixes, count from 0-9->a-z, rinse and repeat
*/
function getNextNameSuffix(currentName: string) {
    let nameCopy = currentName.split("");
    let currentIndex = nameCopy.length - 1;
    let incrementNext = false;
    do {
        let nextCharacterIndex = currentName.charCodeAt(currentIndex);
        nextCharacterIndex++;
        incrementNext = false;

        if (nextCharacterIndex > Z_INDEX) {
            nextCharacterIndex = ZERO_INDEX;
            incrementNext = true;

            // add next digit
            if (currentIndex === 0) {
                nameCopy.unshift(String.fromCharCode(ZERO_INDEX));
                currentIndex++;
            }
        }

        if (nextCharacterIndex > NINE_INDEX && nextCharacterIndex - 1 === NINE_INDEX) {
            nextCharacterIndex = A_INDEX;
        }

        nameCopy[currentIndex] = String.fromCharCode(nextCharacterIndex);
        currentIndex--;
    } while (currentIndex >= 0 && incrementNext);

    return nameCopy.join("");
}

const walletOptions: any = {
    unsafeOptions: {
        skipSynchronizationBeforeHeight: 500000, // only sync from mid-2021
    },
}

if (WALLET_MNEMONIC) {
    walletOptions["mnemonic"] = WALLET_MNEMONIC;
}

// create a new dash client
const walletClient = new Dash.Client({
    network: "testnet",
    wallet: walletOptions
});

const client = new DAPI(walletClient);

// main
(async () => {
    // if you don't have a wallet:
    // await createNewWallet();

    // if you don't have an identity with balance yet:
    // await createAndTopupIdentity();

    // HAS TO BE DONE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    // this syncs the wallet, no better way since isReady() does not exist anymore?
    const wallet = await client.client.getWalletAccount();
    console.log(`Total balance: ${wallet.getTotalBalance()}`)
    createNames(THREAD_COUNT);
})();

async function createNames(threadCount: number = 1) {
    if (threadCount > 34) throw new Error("Invalid thread count!");

    for (let thread = 0; thread < threadCount; thread++) {
        let threadIndex = thread.toString();
        if (thread > 9) {
            const characterIndex = "a".charCodeAt(0) - 1 + thread - 9;
            threadIndex = String.fromCharCode(characterIndex);
        }
        createNameThread(threadIndex);
    }
}

async function createNameThread(threadIndex: string, creationAmount = 10000000001) {
    console.log(`[Thread ${threadIndex}] Starting...`);
    const threadPath = `./data/thread_storage_${threadIndex}.txt`;
    let attempts = 0;
    // create storage file for thread
    if (!fs.existsSync(threadPath)) {
        fs.writeFileSync(threadPath, "0");
    }

    // read current suffix
    let currentThreadSuffix = fs.readFileSync(threadPath).toString();

    // try to create names until the specified creationAmount is reached
    while (attempts < creationAmount) {
        let currentName = PREFIX + MACHINE_INFIX + threadIndex + currentThreadSuffix.padStart(MAX_SUFFIX_LENGTH, "0");
        console.log(`[Thread ${threadIndex}] Trying to register ${currentName}`);
        let successful = false;

        // try to register an alias
        try {
            await client.registerAlias(IDENTITY_ID, currentName);
            successful = true;
        } catch (e: any) {
            console.log(`[Thread ${threadIndex}] ${JSON.stringify(e.message)}`);
        }

        if (successful) {
            console.log(`[Thread ${threadIndex}] Successful!`);
        }

        attempts++;
        currentThreadSuffix = getNextNameSuffix(currentThreadSuffix);

        // store current name every 10 requests
        if (attempts % 10 === 0) {
            console.log(`[Thread ${threadIndex}] Storing current name suffix.... let's go`);
            fs.writeFileSync(threadPath, currentThreadSuffix);
        }

    }
}

async function createNewWallet() {
    const wallet = await client.client.getWalletAccount();
    console.log("Mnemonic: " + client.client.wallet?.exportWallet());
    console.log("Funding adress: " + wallet.getUnusedAddress().address);
}

async function createAndTopupIdentity(topupAmount = 500000) {
    const identity = await client.registerIdentity();
    console.log("Identity ID: " + identity.id);
    await client.topupIdentity(IDENTITY_ID, topupAmount);
}

