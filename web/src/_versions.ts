export interface TsAppVersion {
    version: string;
    name: string;
    description?: string;
    versionLong?: string;
    versionDate: string;
    gitCommitHash?: string;
    gitCommitDate?: string;
    gitTag?: string;
};
export const versions: TsAppVersion = {
    version: '0.0.0',
    name: 'opentakserver-ui',
    versionDate: '2026-01-05T01:26:42.364Z',
    gitCommitHash: '1062a5a',
    versionLong: '0.0.0-1062a5a',
};
export default versions;
