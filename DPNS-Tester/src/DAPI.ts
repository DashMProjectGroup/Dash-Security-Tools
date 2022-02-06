// typesafe DAPI wrapper
import { Client } from "dash/dist/src/SDK/Client";

export class DAPI {
    client: Client;
    constructor(client: Client) {
        this.client = client;
    }

    registerIdentity = async () => {
        return this.client.platform.identities.register();
    }

    topupIdentity = async (identity: string, duffAmount: number = 1000) => {
        await this.client.platform.identities.topUp(identity, duffAmount);
        return this.client.platform.identities.get(identity);
    };

    retrieveIdentities = async () => {
        const wallet = await this.client.getWalletAccount();
        return wallet.identities.getIdentityIds();
    };

    registerName = async (identityId: string, name: string) => {
        const { platform } = this.client;

        const identity = await platform.identities.get(identityId);
        const nameRegistration = await platform.names.register(
            `${name}.dash`,
            { dashUniqueIdentityId: identity.getId() },
            identity,
        );

        return nameRegistration;
    };

    registerAlias = async (identityId: string, name: string) => {
        const platform = this.client.platform;
        const identity = await platform.identities.get(identityId);
        const aliasRegistration = await platform.names.register(
            `${name}.dash`,
            { dashAliasIdentityId: identity.getId() },
            identity,
        );

        return aliasRegistration;
    };

    retrieveName = async (name: string) => {
        return this.client.platform.names.search(name, "dash");
    }

    getWalletBalance = async () => {
        const wallet = await this.client.getWalletAccount();
        return wallet.getConfirmedBalance();
    }

    // retrieve all dash accounts via wildcard query
    getAllDashAccounts = async () => {
        let totalAccounts = 0;
        for (let i = "a".charCodeAt(0); i <= "z".charCodeAt(0); i++) {
            const nameRecord: any[] = await this.retrieveName(String.fromCharCode(i));
            totalAccounts += nameRecord.length;
            nameRecord.forEach(r => console.log(r.data.label));
        }

        for (let i = 0; i <= 9; i++) {
            const nameRecord: any[] = await this.retrieveName(i.toString());
            totalAccounts += nameRecord.length;
            nameRecord.forEach(r => console.log(r.data.label));
        }

        console.log("Total testnet accounts: " + totalAccounts);
    }
}